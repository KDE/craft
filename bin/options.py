# @package property handling
#
# (c) copyright 2009-2011 Ralf Habacker <ralf.habacker@freenet.de>
#
#
#

import atexit
import collections
import configparser
import os
import re
import zlib

import utils
from Blueprints.CraftPackageObject import (
    BlueprintException,
    BlueprintNotFoundException,
    CraftPackageObject,
)
from CraftCore import CraftCore
from CraftDebug import deprecated
from Utils.Arguments import Arguments
from Utils.CraftBool import CraftBool


class RegisteredOption(object):
    def __init__(self, value, compatible):
        self.value = value
        # whether or not this change breaks binary cache compatibility
        self.compatible = compatible

    def __str__(self):
        if callable(self.value):
            return f"({self.value.__name__})"
        else:
            return str(self.value)


class UserOptions(object):
    class UserOptionsSingleton(object):
        _instance = None

        @property
        def __header(self):
            return """\
# The content of this file is partly autogenerated
# You can modify values and add settings for your blueprints
# Common settings available for all blueprints are:
#     ignored: [True|False]
#     version: some version
#     # use the same url as defined for the target but checks out a different branch
#     srcDir: str                                   An absolute path to a source dir to use instead of fetching the source from the targets remote
#     branch: str                                   A branch
#     revision: str                                 A revision or tag, overrides branch
#     patchLevel: int
#     buildType: [Release|RelWithDebInfo|Debug]     The default is defined by CraftSettings.ini [Compile]BuildType
#     buildTests: [True|False]
#     buildTools: [True|False]
#     buildStatic: [True|False]
#     # arguments passed to the configure step
#     args: list[str]
#     # special args passed to qmake
#     featureArguments:  list[str]
#
# Example:
##     [libs]
##     ignored = True
##

##     [libs/qt6]
##     ignored = False
##
##     [libs/qt6/qtbase]
##     version = 6.6.2
##     withPCRE2 = True
##
##     [kde/pim/akonadi]
##     args = -DAKONADI_BUILD_QSQLITE=On
##
#
# Settings are inherited, so you can set them for a whole sub branch or a single blueprint.
# While blueprint from [libs] are all ignored blueprint from [libs/qt6] are not.
#
"""

        def __init__(self):
            self.cachedOptions = {}
            self.packageOptions = {}
            self.registeredOptions = {}  # type: Dict[str : RegisteredOption]

            self.path = CraftCore.settings.get(
                "Blueprints",
                "Settings",
                CraftCore.standardDirs.etcDir() / "BlueprintSettings.ini",
            )
            self.settings = configparser.ConfigParser(allow_no_value=True)
            self.settings.optionxform = str

            if os.path.isfile(self.path):
                self.settings.read(self.path, encoding="utf-8")

        def initPackage(self, option) -> configparser.SectionProxy:
            path = option._package.path
            if not self.settings.has_section(path):
                self.settings.add_section(path)
            settings = self.settings[path]
            return settings

        @staticmethod
        @atexit.register
        def _save():
            instance = UserOptions.UserOptionsSingleton._instance
            if instance:
                try:
                    with open(instance.path, "wt", encoding="utf-8") as configfile:
                        print(instance.__header, file=configfile)
                        instance.settings.write(configfile)
                except Exception as e:
                    CraftCore.log.warning(f"Failed so save {instance.path}: {e}")

    @staticmethod
    def instance():
        if not UserOptions.UserOptionsSingleton._instance:
            UserOptions.UserOptionsSingleton._instance = UserOptions.UserOptionsSingleton()
        return UserOptions.UserOptionsSingleton._instance

    def __init__(self, package):
        self._cachedFromParent = {}
        self._package = package

        _register = self.registerOption
        _convert = self._convert

        # cachability is handled by the version comparison
        _register("version", str, persist=False, compatible=True)
        _register("patchLevel", int, persist=False, compatible=True)

        _register("srcDir", str, persist=False, compatible=True)
        _register("branch", str, persist=False)
        _register("revision", str, persist=False)
        _register("ignored", CraftBool, persist=False, compatible=True)
        _register("buildTests", CraftCore.isNative(), persist=False, compatible=True)
        _register("buildTools", CraftCore.isNative(), persist=False, compatible=True)
        _register("buildStatic", CraftCore.compiler.platform.isIOS, persist=False)

        _register(
            "buildType",
            CraftCore.settings.get("Compile", "BuildType"),
            persist=False,
            compatible=True,
        )  # cachability already handled by cache behaviour
        _register("args", Arguments(), persist=False)
        _register("featureArguments", Arguments(), persist=False)

        settings = UserOptions.instance().settings
        if settings.has_section(package.path):
            _registered = UserOptions.instance().registeredOptions[package.path]
            for key, value in settings[package.path].items():
                if key in _registered:
                    value = _convert(_registered[key].value, value)
                setattr(self, key, value)

    def dump(self) -> collections.OrderedDict:
        out = []
        for key, option in UserOptions.instance().registeredOptions[self._package.path].items():
            atr = getattr(self, key)
            if atr is None:
                atr = option
            out.append((key, str(atr)))
        return collections.OrderedDict(sorted(out))

    def __str__(self):
        return ", ".join([f"{x}={y}" for x, y in self.dump().items()])

    # legacy
    def __configHash(self):
        tmp = []
        for key, _ in self.dump().items():
            # ignore flags that have no influence on the archive
            if not UserOptions.instance().registeredOptions[self._package.path][key].compatible:
                atr = getattr(self, key)
                if atr is not None:
                    if key == "buildType":
                        # Releaseand and RelWithDebInfo are compatible
                        atr = 1 if atr in {"Release", "RelWithDebInfo"} else 0
                    tmp.append(key.encode())
                    tmp.append(bytes(atr, "UTF-8") if isinstance(atr, str) else bytes([atr]))
        return zlib.adler32(b"".join(tmp))

    def __isUserSet(self, key):
        return key in UserOptions.instance().initPackage(self)

    def compatible(self, other: collections.OrderedDict, hash=None) -> bool:
        if not other and hash:
            return self.__configHash() == hash
        for key, value in self.dump().items():
            # ignore flags that have no influence on the archive
            if not UserOptions.instance().registeredOptions[self._package.path][key].compatible:
                if key not in other:
                    # a new key but is empty, False is a new value and needs to be handled
                    if not value and value is not False:
                        continue
                    CraftCore.log.info(f"Config is not compatible: {key} is a new option")
                    return False
                elif key == "buildType":
                    # Releaseand and RelWithDebInfo are compatible
                    if value == "Debug" and other[key] != "Debug":
                        CraftCore.log.info(f"Config is not compatible: {key} {value} != {other[key]}")
                        return False
                elif value != other[key]:
                    CraftCore.log.info(f"Config is not compatible: {key} {value} != {other[key]}")
                    return False
        return True

    @staticmethod
    def get(package):
        _instance = UserOptions.instance()
        packagePath = package.path
        if packagePath in _instance.cachedOptions:
            option = _instance.cachedOptions[packagePath]
        else:
            option = UserOptions(package)
            _instance.cachedOptions[packagePath] = option
        return option

    def _convert(self, valA, valB):
        """
        Converts valB to type(valA)
        """
        try:
            if valA is None:
                return valB
            if isinstance(valB, str) and hasattr(valA, "fromSetting"):
                return valA.fromSetting(valB)
            _type = valA if callable(valA) else type(valA)
            if _type == type(valB):
                return valB
            if _type is bool:
                return CraftBool(valB)
            return _type(valB)
        except Exception as e:
            CraftCore.log.error(f"Can't convert {valB} to {_type.__name__}")
            raise e

    @staticmethod
    def setOptions(optionsIn):
        """
        set temporary options from string
        craft global options in the form of [Section]Key=Value
        package options in the from of libs/libpng.Key=Value
        the options are not persisted
        """
        sectionRe = re.compile(r"\[([^\[\]]+)\](.*)")
        for o in optionsIn:
            key, value = o.split("=", 1)
            key, value = key.strip(), value.strip()
            match = sectionRe.findall(key)
            if match:
                # TODO: move out of options.py
                section, key = match[0]
                CraftCore.log.info(f"setOptions: [{section}]{key} = {value}")
                CraftCore.settings.set(section, key, value)
            else:
                package, key = key.split(".", 1)
                packageObject = CraftPackageObject.get(package)
                if packageObject:
                    UserOptions.addPackageOption(packageObject, key, value)
                    CraftCore.log.info(f"setOptions: BlueprintSettings.ini [{package}]{key} = {value}")
                else:
                    raise BlueprintNotFoundException(
                        package,
                        f"Package {package} not found, failed to set option {key} = {value}",
                    )

    @staticmethod
    def addPackageOption(package: CraftPackageObject, key: str, value: str) -> None:
        """
        Set non persistant options on a package
        """
        if package.path not in UserOptions.instance().packageOptions:
            UserOptions.instance().packageOptions[package.path] = {}
        if package.path in UserOptions.instance().cachedOptions:
            UserOptions.instance().cachedOptions[package.path]._cachedFromParent = {}
        UserOptions.instance().packageOptions[package.path][key] = value

    def setOption(self, key, value, persist: bool = True) -> bool:
        _instance = UserOptions.instance()  # type: UserOptions.UserOptionsSingleton
        package = self._package
        if package.path not in _instance.registeredOptions:  # actually that can only happen if package is invalid
            CraftCore.log.error(f"{package} has no options")
            return False
        if key not in _instance.registeredOptions[package.path]:
            CraftCore.log.error(f"{package} unknown option {key}")
            CraftCore.log.error("Valid options are")
            for optionKey, defaultOption in _instance.registeredOptions[package.path].items():
                default = defaultOption.value
                default = default if callable(default) else type(default)
                CraftCore.log.error(f"\t{default.__name__} : {optionKey}")
            return False
        settings = _instance.initPackage(self)
        if value == "":
            if key in settings:
                if persist:
                    del settings[key]
                delattr(self, key)
            if not settings.keys():
                del _instance.settings[self._package.path]
        else:
            value = self._convert(_instance.registeredOptions[package.path][key].value, value)
            if persist:
                if hasattr(value, "toSetting"):
                    settings[key] = value.toSetting()
                else:
                    settings[key] = str(value)
            setattr(self, key, value)
        return True

    def registerOption(self, key: str, default, persist: bool = True, compatible: bool = False) -> bool:
        _instance = UserOptions.instance()
        package = self._package
        if package.path not in _instance.registeredOptions:
            _instance.registeredOptions[package.path] = {}
        if key in _instance.registeredOptions[package.path]:
            raise BlueprintException(
                f"Failed to register option:\n[{package}]\n{key}={default}\nThe setting {key} is already registered.",
                package,
            )
            return False
        if isinstance(default, bool):
            default = CraftBool(default)
        _instance.registeredOptions[package.path][key] = RegisteredOption(default, compatible)
        if persist:
            settings = _instance.initPackage(self)
            if key and key not in settings:
                settings[key] = str(default)

            # don't try to save types
            if not callable(default):
                if not hasattr(self, key):
                    setattr(self, key, default)
                else:
                    # convert type
                    old = getattr(self, key)
                    try:
                        new = self._convert(default, old)
                    except Exception as e:
                        raise BlueprintException(
                            f"Found an invalid option in BlueprintSettings.ini,\n[{self._package}]\n{key}={old}", self._package, exception=e
                        )
                    # print(key, type(old), old, type(new), new)
                    setattr(self, key, new)
        return True

    def setDefault(self, key: str, default) -> bool:
        _instance = UserOptions.instance()
        package = self._package
        if key not in _instance.registeredOptions[package.path]:
            raise BlueprintException(
                f"Failed to set default for unregistered option: [{package}]{key}.",
                package,
            )
        if not self.__isUserSet(key):
            return self.setOption(key, default, persist=False)
        return True

    def __getattribute__(self, name):
        if name.startswith("_"):
            return super().__getattribute__(name)
        try:
            member = super().__getattribute__(name)
        except AttributeError:
            member = None
        if member and callable(member):
            return member

        # check cache
        _cache = self._cachedFromParent
        if not member and name in _cache:
            return _cache[name]

        out = None
        _instance = UserOptions.instance()
        _package = self._package
        _packagePath = _package.path
        if _packagePath in _instance.packageOptions and name in _instance.packageOptions[_packagePath]:
            if _packagePath not in _instance.registeredOptions or name not in _instance.registeredOptions[_packagePath]:
                raise BlueprintException(f"Package {_package} has no registered option {name}", _package)
            out = self._convert(
                _instance.registeredOptions[_packagePath][name].value,
                _instance.packageOptions[_packagePath][name],
            )
        elif member is not None:
            # value is not overwritten by comand line options
            return member
        else:
            parent = _package.parent
            if parent:
                out = getattr(UserOptions.get(parent), name)

        if out is None:
            # name is a registered option and not a type but a default value
            if _packagePath in _instance.registeredOptions and name in _instance.registeredOptions[_packagePath]:
                default = _instance.registeredOptions[_packagePath][name].value
                if not callable(default):
                    out = default

        # skip lookup in command line options and parent objects the enxt time
        _cache[name] = out
        # print("added to cache", _packagePath, name, type(out), out)
        return out


class OptionsBase(object):
    def __init__(self):
        pass


# options for the fetch action
class OptionsFetch(OptionsBase):
    def __init__(self):
        # option comment
        self.option = None
        self.ignoreExternals = False
        # enable submodule support in git single branch mode
        self.checkoutSubmodules = False


# options for the unpack action
class OptionsUnpack(OptionsBase):
    def __init__(self):
        #  Use this option to run 3rd party installers
        self.runInstaller = False
        # CMake on Windows still has no proper support for symlinks, so we replace them with copies
        # The option is only supported on Windows
        self.keepSymlinksOnWindows = False


# options for the configure action
class OptionsConfigure(OptionsBase):
    def __init__(self, dynamic):
        # with this option additional arguments could be added to the configure commmand line
        self.args = Arguments(dynamic.args)
        # with this option additional arguments could be added to the configure commmand line (for static builds)
        self.staticArgs = Arguments()
        # set source subdirectory as source root for the configuration tool.
        # Sometimes it is required to take a subdirectory from the source tree as source root
        # directory for the configure tool, which could be enabled by this option. The value of
        # this option is added to sourceDir() and the result is used as source root directory.
        self.configurePath = None

        # add the cmake defines that are needed to build tests here
        self.testDefine = None

        # add the cmake defines that are needed to build tools (if buildTools is True)
        self.toolsDefine = None

        # run autogen in autotools
        self.bootstrap = False

        # run "autoreconf -vfi" in autotools
        self.autoreconf = True

        # optional arguments for autoreconf
        self.autoreconfArgs = Arguments(["-vfi"])

        # Whether to add the default -I flags when running autoreconf
        # This is needed since some packages fail if we pass -I to autoreconf
        self.useDefaultAutoreconfIncludes = True

        # do not use default include path
        self.noDefaultInclude = False

        # do not use default lib path
        self.noDefaultLib = False

        # set this attribute in case a non standard configuration
        # tool is required (supported currently by QMakeBuildSystem only)
        self.tool = False

        # cflags currently only used for autotools
        self.cflags = ""

        # cxxflags currently only used for autotools
        self.cxxflags = ""

        # ldflags currently only used for autotools
        self.ldflags = ""

        # the project file, this is either a .pro for qmake or a sln for msbuild
        self.projectFile = None

        # whether to not pass --datarootdir configure
        self.noDataRootDir = False

        # whether to not pass --libdir configure
        self.noLibDir = False

        # whether to not pass --cache-file configure
        self.noCacheFile = False


# options for the make action
class OptionsMake(OptionsBase):
    def __init__(self):
        # ignore make error
        self.ignoreErrors = None
        # options for the make tool
        self.args = Arguments()
        self.supportsMultijob = True

    @property
    @deprecated("options.make.args")
    def makeOptions(self):
        return self.args

    @makeOptions.setter
    @deprecated("options.make.args")
    def makeOptions(self, x):
        self.args = x


class OptionsInstall(OptionsBase):
    def __init__(self):
        # options passed to make on install
        self.args = Arguments(["install"])


# options for the package action
class OptionsPackage(OptionsBase):
    def __init__(self):
        # defines the package name
        self.packageName = None
        # defines the package version
        self.version = None
        # use compiler in package name
        self.withCompiler = True
        # use special packaging mode  (only for qt)
        self.specialMode = False
        # pack also sources
        self.packSources = True
        # pack from subdir of imageDir()
        # currently supported by SevenZipPackager
        self.packageFromSubDir = None
        # use architecture in package name
        # currently supported by SevenZipPackager
        self.withArchitecture = False
        # add file digests to the package located in the manifest sub dir
        # disable stripping of binary files
        # needed for mysql, striping make the library unusable
        self.disableStriping = False

        # disable the binary cache for this package
        self.disableBinaryCache = False

        # whether to move the plugins to bin
        self.movePluginsToBin = utils.OsUtils.isWin()
        # whether to move the translations to bin
        self.moveTranslationsToBin = utils.OsUtils.isWin()


# main option class
class Options(object):
    def __init__(self, package=None):
        self.dynamic = UserOptions.get(package)
        # options of the fetch action
        self.fetch = OptionsFetch()
        # options of the unpack action
        self.unpack = OptionsUnpack()
        # options of the configure action
        self.configure = OptionsConfigure(self.dynamic)
        self.make = OptionsMake()
        self.install = OptionsInstall()
        # options of the package action
        self.package = OptionsPackage()
        # add the date to the target
        self.dailyUpdate = False

        # there is a special option available already
        self.useShadowBuild = True

    @property
    def buildStatic(self):
        return self.dynamic.buildStatic

    def isActive(self, package) -> CraftBool:
        if isinstance(package, str):
            package = CraftPackageObject.get(package)
        # init the subinfo
        package.instance
        return package.isIgnored().inverted
