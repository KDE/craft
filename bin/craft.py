#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# this will craft some programs...

# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>
# Hannah von Reth <vonreth [AT] kde [DOT] org>

# The minimum python version for craft please edit here
# if you add code that changes this requirement

import argparse
import collections

import CraftSetupHelper
import InstallDB
import blueprintSearch
import utils
from CraftConfig import *
from Blueprints.CraftDependencyPackage import CraftDependencyPackage
from Blueprints.CraftPackageObject import *
from Blueprints.CraftVersion import CraftVersion
from Utils import CraftTimer
from Utils.CraftTitleUpdater import CraftTitleUpdater

if not "KDEROOT" in os.environ:
    helper = CraftSetupHelper.SetupHelper()
    helper.subst()
    helper.setupEnvironment()
    helper.printBanner()


def migrate():
    portageDir = os.path.join(CraftStandardDirs.etcDir(), "portage")
    if os.path.isdir(portageDir):
        del CraftCore.installdb
        utils.moveEntries(portageDir, CraftStandardDirs.etcBlueprintDir())
        utils.rmtree(portageDir)
        CraftCore.installdb =InstallDB.InstallDB()
    CraftCore.installdb.migrateDatabase()


def destroyCraftRoot():
    del CraftCore.installdb
    root = CraftStandardDirs.craftRoot()
    for entry in os.listdir(root):
        path = os.path.join(root, entry)
        if os.path.exists(CraftStandardDirs.etcDir()) and os.path.samefile(path, CraftStandardDirs.etcDir()):
            for entry in os.listdir(path):
                if entry not in ["kdesettings.ini", "CraftSettings.ini"]:
                    etcPath = os.path.join(path, entry)
                    if os.path.isdir(etcPath):
                        if utils.OsUtils.isLink(etcPath):
                            print("Skipping symlink %s" % etcPath)
                            continue
                        utils.cleanDirectory(etcPath)
                        utils.OsUtils.rmDir(etcPath, True)
                    else:
                        utils.OsUtils.rm(etcPath, True)
        elif not any(os.path.exists(x) and os.path.samefile(path, x) for x in [CraftStandardDirs.downloadDir(),
                                                                               os.path.normpath(os.path.join(
                                                                                       CraftStandardDirs.craftBin(),
                                                                                       "..")),
                                                                               os.path.join(
                                                                                   CraftStandardDirs.craftRoot(),
                                                                                   "python")]):
            if utils.OsUtils.isLink(path):
                print("Skipping symlink %s" % path)
                continue
            utils.cleanDirectory(path)
            utils.OsUtils.rmDir(path, True)


def readListFile(listFile):
    packageNames = []
    parser = configparser.ConfigParser(allow_no_value=True)
    parser.read(listFile)
    for sections in parser.keys():
        for packageName in parser[sections]:
            CraftCore.settings.set("BlueprintVersions", packageName, parser.get(sections, packageName))
            packageNames.append(packageName)
    return packageNames


def packageIsOutdated(package):
    installed = CraftCore.installdb.getInstalledPackages(package)
    if not installed:
        return True
    for pack in installed:
        version = pack.getVersion()
        if not version: continue
        return CraftVersion(package.version) > CraftVersion(version)

def doExec(package, action, continueFlag=False):
    with CraftTimer.Timer("%s for %s" % (action, package), 1):
        CraftCore.debug.step("Action: %s for %s" % (action, package))
        ret = package.instance.execute(action)
        if not ret:
            CraftCore.log.warning("Action: %s for %s FAILED" % (action, package))
        return ret or continueFlag


def handlePackage(package, buildAction, continueFlag, directTargets):
    with CraftTimer.Timer(f"HandlePackage {package}", 3) as timer:
        CraftCore.debug.debug_line()
        CraftCore.debug.step(f"Handling package: {package}, action: {buildAction}")

        success = True

        if buildAction == "all":
            if CraftCore.settings.getboolean("Packager", "UseCache", "False") \
                    and not package.isVirtualPackage():
                if doExec(package, "fetch-binary"):
                    return True
            success = success and doExec(package, "fetch", continueFlag)

            success = success and doExec(package, "unpack", continueFlag)
            success = success and doExec(package, "compile")
            success = success and doExec(package, "cleanimage")
            success = success and doExec(package, "install")
            if buildAction == "all":
                success = success and doExec(package, "qmerge")
            if CraftCore.settings.getboolean("Packager", "CreateCache"):
                if CraftCore.settings.getboolean("Packager", "CacheDirectTargetsOnly"):
                    nameRe = re.compile(".*\/.*")
                    for target in directTargets:
                        if not nameRe.match(target):
                            CraftCore.log.error("Error:\n"
                                                 "[Packager]\n"
                                                 "CacheDirectTargetsOnly = True\n"
                                                 "Only works with fully specified packages 'category/package'")
                            return False
                    if package in directTargets:
                        success = success and doExec(package, "package")
                    else:
                        CraftCore.log.info("skip packaging of non direct targets")
                else:
                    success = success and doExec(package, "package")
            success = success or continueFlag
        elif buildAction in ["fetch", "fetch-binary", "unpack", "configure", "compile", "make",
                             "test", "package", "unmerge", "createpatch", "print-files" ]:
            success = doExec(package, buildAction, continueFlag)
        elif buildAction == "install":
            success = doExec(package, "cleanimage")
            success = success and doExec(package, "install", continueFlag)
        elif buildAction == "qmerge":
            success = success and doExec(package, "qmerge")
        else:
            success = CraftCore.log.error("could not understand this buildAction: %s" % buildAction)

        timer.stop()
        utils.notify(f"Craft {buildAction} {'succeeded' if success else 'failed'}",
                     f"{package} after {timer}", buildAction)
        return success


def run(package, action, args, directTargets):
    if package.isIgnored():
        CraftCore.log.info(f"Skipping package because it has been ignored: {package}")
        return True

    if action == "get":
        key = args.get.replace("()", "")
        isMethode = args.get.endswith("()")
        for p in directTargets:
            instance = p.instance
            if hasattr(instance, key.replace("()", "")):
                attr = getattr(instance, key)
                if isMethode:
                    value = attr()
                else:
                    value = attr
                CraftCore.log.debug(value)
                print(value)
                return True
            else:
               CraftCore.log.debug(f"{p} has no member {key}")
               print(f"{p} has no member {key}", file=sys.stderr)
               return False
    elif action not in ["all", "install-deps"]:
        for info in package.children.values():
           # not all commands should be executed on the deps if we are a virtual packages
            # if a buildAction is given, then do not try to build dependencies
            # and do the action although the package might already be installed.
            # This is still a bit problematic since packageName might not be a valid
            # package
            # for list files, we also want to handle fetching & packaging per package
            if not handlePackage(info, action, args.doContinue,
                                 directTargets=directTargets):
                return False

    else:
        depPackage = CraftDependencyPackage(package)
        depList = depPackage.getDependencies()

        packages = []
        for item in depList:
            if (args.ignoreInstalled and item in directTargets) or packageIsOutdated(item):
                packages.append(item)
                CraftCore.log.debug(f"dependency: {item}")
        if not packages:
            CraftCore.log.debug("<none>")

        if action == "install-deps":
            # we don't intend to build the package itself
            for x in directTargets:
                packages.remove(x)

        CraftTitleUpdater.usePackageProgressTitle(packages)
        while packages:
            info = packages[0]
            # in case we only want to see which packages are still to be build, simply return the package name
            if args.probe:
                CraftCore.log.warning(f"pretending {info}: {info.version}")
            else:
                if CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False):
                    CraftCore.debug.debug_line()
                    CraftCore.log.info(f"Status: {CraftTitleUpdater.instance}")
                if action in ["install-deps"]:
                    action = "all"

                if not handlePackage(info, action, args.doContinue,
                                     directTargets=directTargets):
                    CraftCore.log.error(f"fatal error: package {info} {action} failed")
                    return False
            packages.pop(0)

    CraftCore.debug.new_line()
    return True


class ActionHandler:
    class StoreTrueAction(argparse._StoreTrueAction):
        def __call__(self, parser, namespace, values, option_string=None):
            ActionHandler.StoreAction._addOrdered(namespace, self.dest, self.const)
            super().__call__(parser, namespace, values, option_string)

    class StoreAction(argparse._StoreAction):
        """http://stackoverflow.com/a/9028031"""

        def __call__(self, parser, namespace, values, option_string=None):
            ActionHandler.StoreAction._addOrdered(namespace, self.dest, values)
            super().__call__(parser, namespace, values, option_string)

        @staticmethod
        def _addOrdered(namespace, key, value):
            if not 'ordered_args' in namespace:
                setattr(namespace, 'ordered_args', collections.OrderedDict())
            namespace.ordered_args[key] = value

    def __init__(self, parser):
        self.parser = parser
        self.actions = {}

    def _addAction(self, actionName, help=None, **kwargs):
        arg = self.parser.add_argument("--%s" % actionName,
                                       help="[Action] %s" % (help if help else ""), **kwargs)
        self.actions[arg.dest] = actionName

    def addAction(self, actionName, **kwargs):
        self._addAction(actionName, action=ActionHandler.StoreTrueAction, **kwargs)

    def addActionWithArg(self, actionName, **kwargs):
        self._addAction(actionName, action=ActionHandler.StoreAction, **kwargs)

    def parseFinalAction(self, args, defaultAction):
        '''Returns the list of actions or [defaultAction]'''
        return [self.actions[x] for x in args.ordered_args.keys()] if hasattr(args, "ordered_args") else [defaultAction]


def main():
    parser = argparse.ArgumentParser(prog="Craft",
                                     description="Craft is an open source meta build system and package manager."
                                                 "It manages dependencies and builds libraries and applications from source, on Windows, Mac, Linux and FreeBSD.",
                                     epilog="For more information visit https://community.kde.org/Craft.\n"
                                            "Send feedback to <kde-windows@kde.org>.")

    parser.add_argument("-p", "--probe", action="store_true",
                        help="probing: craft will only look which files it has to build according to the list of installed files and according to the dependencies of the package.")
    parser.add_argument("--list-file", action="store",
                        help="Build all packages from the ini file provided")
    parser.add_argument("--options", action="append",
                        default=CraftCore.settings.getList("General", "Options", ""),
                        help="Set craft property from string <OPTIONS>. An example for is \"cmake.openIDE=1\" see options.py for more informations.")
    parser.add_argument("-q", "--stayquiet", action="store_true",
                        dest="stayQuiet",
                        help="quiet: there should be no output - The verbose level should be 0")
    parser.add_argument("-c", "--continue", action="store_true", dest="doContinue")
    parser.add_argument("--create-cache", action="store_true", dest="createCache",
                        default=CraftCore.settings.getboolean("Packager", "CreateCache", "False"),
                        help="Create a binary cache, the setting is overwritten by --no-cache")
    parser.add_argument("--use-cache", action="store_true", dest="useCache",
                        default=CraftCore.settings.getboolean("Packager", "UseCache", "False"),
                        help="Use a binary cache, the setting is overwritten by --no-cache")
    parser.add_argument("--no-cache", action="store_true", dest="noCache",
                        default=False, help="Don't create or use the binary cache")
    parser.add_argument("--destroy-craft-root", action="store_true", dest="doDestroyCraftRoot",
                        default=False,
                        help="DANGEROUS: Recursively delete everything in the Craft root directory besides the CraftSettings.ini, the download directory and the craft folder itself")
    parser.add_argument("--offline", action="store_true",
                        default=CraftCore.settings.getboolean("General", "WorkOffline", False),
                        help="do not try to connect to the internet: KDE packages will try to use an existing source tree and other packages would try to use existing packages in the download directory.\
                          If that doesn't work, the build will fail.")
    parser.add_argument("--buildtype", choices=["Release", "RelWithDebInfo", "MinSizeRel", "Debug"],
                        dest="buildType",
                        default=CraftCore.settings.get("Compile", "BuildType", "RelWithDebInfo"),
                        help="This will override the build type set in your CraftSettings.ini.")
    parser.add_argument("-v", "--verbose", action="count",
                        default=int(CraftCore.settings.get("CraftDebug", "Verbose", "0")),
                        help=" verbose: increases the verbose level of craft. Default is 1. verbose level 1 contains some notes from craft, all output of cmake, make and other programs that are used.\
                          verbose level 2a dds an option VERBOSE=1 to make and craft is more verbose highest level is verbose level 3.")
    parser.add_argument("-i", "--ignoreInstalled", action="store_true",
                        help="ignore install: using this option will install a package over an existing install. This can be useful if you want to check some new code and your last build isn't that old.")
    parser.add_argument("--target", action="store",
                        help="This will override the build of the default target.")
    parser.add_argument("--search", action="store_true",
                        help="This will search for a package or a description matching or similar to the search term.")
    parser.add_argument("--log-dir", action="store",
                        default=CraftCore.settings.get("CraftDebug", "LogDir", os.path.expanduser("~/.craft/")),
                        help="This will log the build output to a logfile in LOG_DIR for each package. Logging information is appended to existing logs.")
    parser.add_argument("--src-dir", action="store", dest="srcDir",
                        help="This will override the source dir and enable the offline mode")

    parser.add_argument("--ci-mode", action="store_true",
                        default=CraftCore.settings.getboolean("ContinuousIntegration", "Enabled", False),
                        dest="ciMode", help="Enables the ci mode")

    actionHandler = ActionHandler(parser)
    for x in sorted(["fetch", "fetch-binary", "unpack", "configure", "compile", "make",
                     "install", "install-deps", "qmerge", "package", "unmerge", "test", "createpatch"]):
        actionHandler.addAction(x)

    # read-only actions
    actionHandler.addAction("print-installed",
                            help="This will show a list of all packages that are installed currently.")
    actionHandler.addAction("print-files", help="Print the files installed by the package and exit")
    actionHandler.addActionWithArg("search-file", help="Print packages owning the file")
    actionHandler.addActionWithArg("get", help="Get any value from a recipe")

    # other actions

    parser.add_argument("--version", action="version", version = f"%(prog)s {CraftSetupHelper.SetupHelper.CraftVersion}")
    parser.add_argument("packageNames", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if args.doDestroyCraftRoot:
        destroyCraftRoot()
        return True

    migrate()

    if args.stayQuiet:
        CraftCore.debug.setVerbose(-1)
    elif args.verbose:
        CraftCore.debug.setVerbose(args.verbose)

    CraftCore.settings.set("General", "WorkOffline", args.offline or args.srcDir is not None)
    CraftCore.settings.set("Compile", "BuildType", args.buildType)
    CraftCore.settings.set("General", "Options", ";".join(args.options))
    CraftCore.settings.set("CraftDebug", "LogDir", args.log_dir)
    CraftCore.settings.set("Packager", "CreateCache", not args.noCache and args.createCache)
    CraftCore.settings.set("Packager", "UseCache", not args.noCache and args.useCache)
    CraftCore.settings.set("ContinuousIntegration", "SourceDir", args.srcDir)
    CraftCore.settings.set("ContinuousIntegration", "Enabled", args.ciMode)

    if CraftCore.settings.getboolean("Packager", "CreateCache"):
        # we are in cache creation mode, ensure to create a 7z image and not an installer
        CraftCore.settings.set("Packager", "PackageType", "SevenZipPackager")

    CraftPackageObject.options = args.options
    if args.search:
        for package in args.packageNames:
            blueprintSearch.printSearch(package)
        return True

    for action in actionHandler.parseFinalAction(args, "all"):
        tempArgs = copy.deepcopy(args)

        if action in ["install-deps", "package"]:
            tempArgs.ignoreInstalled = True

        CraftCore.log.debug("buildAction: %s" % action)
        CraftCore.log.debug("doPretend: %s" % tempArgs.probe)
        CraftCore.log.debug("packageName: %s" % tempArgs.packageNames)
        CraftCore.log.debug("buildType: %s" % tempArgs.buildType)
        CraftCore.log.debug("verbose: %d" % CraftCore.debug.verbose())
        CraftCore.log.debug("Craft: %s" % CraftStandardDirs.craftRoot())

        packageNames = tempArgs.packageNames
        if tempArgs.list_file:
            if not packageNames:
                packageNames = []
            packageNames += readListFile(args.list_file)

        if action == "print-installed":
            InstallDB.printInstalled()
        elif action == "search-file":
            InstallDB.printPackagesForFileSearch(tempArgs.search_file)
        else:
            if not args.packageNames and not args.list_file:
                CraftSetupHelper.SetupHelper().printBanner()
                return True

            package = CraftPackageObject(None)
            for packageName in packageNames:
                child = CraftPackageObject.get(packageName)
                if not child:
                    blueprintSearch.printSearch(packageName)
                    return False

                if child.isCategory():
                    package.children.update(child.children)
                else:
                    if tempArgs.target:
                        CraftCore.settings.set("BlueprintVersions", child.path, args.target)
                    package.children[child.name] = child
            if not run(package, action, tempArgs, package.children.values()):
                return False
    return True


if __name__ == '__main__':
    success = False
    with CraftTimer.Timer("Craft", 0) as timer:
        CraftTitleUpdater.instance = CraftTitleUpdater()
        if not "CRAFT_NOTITLEUPDATE" in os.environ:
            CraftTitleUpdater.instance.start(f"({CraftStandardDirs.craftRoot()}) craft " + " ".join(sys.argv[1:]), timer)
        try:
            success = main()
        except KeyboardInterrupt:
            pass
        except BlueprintException as e:
            if 0 <= CraftCore.debug.verbose() < 2:
                CraftCore.log.error(e)
                CraftCore.log.debug(e, exc_info=e.exception or e)
            else:
                CraftCore.log.error(e, exc_info=e.exception or e)
        except Exception as e:
            CraftCore.log.error(e, exc_info=e)
        finally:
            CraftTitleUpdater.instance.stop()
    if not success:
        exit(1)
