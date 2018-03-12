#!/usr/bin/env python
import copy
import importlib
import os
import re
import configparser

import CraftConfig
from CraftStandardDirs import CraftStandardDirs
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
import utils

class CategoryPackageObject(object):
    def __init__(self, localPath : str):
        self.localPath = localPath
        self.desctiption = ""
        self.platforms = {}

        ini = os.path.join(self.localPath, "info.ini")
        if os.path.exists(ini):
            info = configparser.ConfigParser()
            info.read(ini)
            self.desctiption = info["General"].get("description", "")
            self.platforms = set(CraftCore.settings._parseList(info["General"].get("platforms", "")))

    @property
    def isActive(self) -> bool:
        return not self.platforms or CraftCore.compiler.platform in self.platforms

class CraftPackageObject(object):
    __rootPackage = None
    __rootDirectories = []
    _recipes = {}#all recipes, for lookup by package name
    IgnoredDirectories = {"__pycache__"}
    Ignores = re.compile("a^")

    @staticmethod
    def _isDirIgnored(d):
        return d.startswith(".") or d in CraftPackageObject.IgnoredDirectories

    def __init__(self, other=None, parent=None):
        if isinstance(other, CraftPackageObject):
            self.__dict__ = other.__dict__
            return
        if other and not parent:
            raise Exception("Calling CraftPackageObject(str) directly is not supported,"
                            " use CraftPackageObject.get(str) instead.")

        self.parent = parent
        self.name = other
        self.children = {}
        self.source = None
        self._version = None
        self._instance = None
        self.__path = None

    @property
    def path(self):
        if self.name == "/":
            return "/"
        if not self.__path:
            components = []
            package = self
            while package:
                if not package.name:
                    break
                components.append(package.name)
                package = package.parent
            if components:
                components.pop(-1)
                components.reverse()
                self.__path = "/".join(components)
        return self.__path

    @staticmethod
    def get(path):
        if isinstance(path, CraftPackageObject):
            return path
        root = CraftPackageObject.root()
        package = None
        if path in CraftPackageObject._recipes:
            packages = CraftPackageObject._recipes[path]
            if len(packages) > 1:
                CraftCore.log.info(f"Found multiple recipes for {path}")
                for p in packages:
                    CraftCore.log.info(p)
                CraftCore.log.info(f"Please use the full path to the recipe.")
                exit(1)
            package = packages[0]
        else:
            components = path.split("/")
            package = root
            for part in components:
                package = package.children.get(part, None)
                if not package:
                    return None
        return package

    @staticmethod
    def _addNode(path, parent, blueprintRoot):
        if path:
            path = utils.normalisePath(path)
            name = path.rsplit("/", 1)[-1]
            if name in parent.children:
                package = parent.children[name]
            else:
                package = CraftPackageObject(name, parent)
        elif blueprintRoot:
            path = blueprintRoot
            package = parent
        else:
            return None

        for f in os.listdir(path):
            fPath = os.path.abspath(os.path.join(path, f))
            if os.path.isdir(fPath):
                if not CraftPackageObject._isDirIgnored(f):
                    hasChildren = True
                    child = CraftPackageObject._addNode(fPath, package, blueprintRoot)
                    if child:
                        if f in package.children:
                            existingNode = package.children[f]
                            if not existingNode.isCategory():
                                CraftCore.log.warning(
                                    f"Blueprint clash detected: Ignoring {child.source} in favour of {existingNode.source}")
                                continue
                            else:
                                #merge with existing node
                                existingNode.children.update(child.children)
                                continue
                        package.children[f] = child
            elif f.endswith(".py"):
                if package.source:
                    raise BlueprintException(f"Multiple py files in one directory: {package.source} and {f}", package)
                if f[:-3] != package.name:
                    raise BlueprintException(f"Recipes must match the name of the directory: {fPath}", package)
                package.source = fPath
        if package.children:
            if package.source:
                raise BlueprintException(f"{package} has has children but also a recipe {package.source}!", package)
            else:
                catInfo = CategoryPackageObject(path)
                if not catInfo.isActive:
                    CraftCore.log.debug(f"Skipping {package.path}, it's not supported on {CraftCore.compiler.platform}")
                    return None

        if path != blueprintRoot:
            if not package.source and not package.children:
                if os.listdir(path) in [["__pycache__"], []]:
                    # the recipe was removed
                    utils.rmtree(path)
                else:
                    CraftCore.log.warning(f"Found an dead branch in {blueprintRoot}/{package.path}\n"
                                       f"You might wan't to run \"git clean -xdf\" in that directry.")
                return None
        return package

    @staticmethod
    def rootDirectories():
        # this function should return all currently set blueprint directories
        if not CraftPackageObject.__rootDirectories:
            rootDirs = {utils.normalisePath(CraftStandardDirs.craftRepositoryDir())}
            if ("Blueprints", "Locations") in CraftCore.settings:
                for path in CraftCore.settings.getList("Blueprints", "Locations"):
                    rootDirs.add(utils.normalisePath(path))
            if os.path.isdir(CraftStandardDirs.blueprintRoot()):
                for f in os.listdir(CraftStandardDirs.blueprintRoot()):
                    if CraftPackageObject._isDirIgnored(f):
                        continue
                    rootDirs.add(utils.normalisePath(os.path.join(CraftStandardDirs.blueprintRoot(), f)))
            CraftCore.log.debug(f"Craft BlueprintLocations: {rootDirs}")
            CraftPackageObject.__rootDirectories = list(rootDirs)
        return CraftPackageObject.__rootDirectories

    @staticmethod
    def bootstrapping() -> bool:
        return len(CraftPackageObject.rootDirectories()) == 1

    @staticmethod
    def __regiserNodes(package):
            for child in package.children.values():
                # hash children for direct acces
                CraftCore.log.debug(f"Adding package {child.source}")
                if not child.isCategory():
                    if child.name not in CraftPackageObject._recipes:
                        CraftPackageObject._recipes[child.name] = []
                    CraftPackageObject._recipes[child.name].append(child)
                CraftPackageObject.__regiserNodes(child)

    @staticmethod
    def root():
        if not CraftPackageObject.__rootPackage:
            if ("Blueprints", "Ignores") in CraftCore.settings:
                CraftPackageObject.Ignores = re.compile("|".join([f"^{entry}$" for entry in CraftCore.settings.get("Blueprints", "Ignores").split(";")]))

            CraftPackageObject.__rootPackage = root = CraftPackageObject()
            root.name = "/"
            for blueprintRoot in CraftPackageObject.rootDirectories():
                if not os.path.isdir(blueprintRoot):
                    CraftCore.log.warning(f"{blueprintRoot} does not exist")
                    continue
                blueprintRoot = utils.normalisePath(os.path.abspath(blueprintRoot))
                # create a dummy package to load its children
                child = CraftPackageObject._addNode(None, root, blueprintRoot)
                root.children.update(child.children)
            CraftPackageObject.__regiserNodes(root)
        return CraftPackageObject.__rootPackage

    @property
    def instance(self):
        if not self._instance:
            CraftCore.log.debug(f"module to import: {self.source} {self.path}")
            modulename = os.path.splitext(os.path.basename(self.source))[0].replace('.', '_')
            loader = importlib.machinery.SourceFileLoader(modulename, self.source)
            try:
                mod = loader.load_module()
            except Exception as e:
                raise BlueprintException(f"Failed to load file {self.source}", self, e)
            if not mod is None:
                mod.CRAFT_CURRENT_MODULE = self
                pack = mod.Package()
                self._instance = pack
            else:
                raise BlueprintException("Failed to find package", self)
        return self._instance

    @property
    def isInstalled(self) -> bool:
        return len(CraftCore.installdb.getInstalledPackages(self)) == 1

    @property
    def subinfo(self):
        return self.instance.subinfo


    def isVirtualPackage(self):
        """ check if that package is of VirtualPackageBase """
        if self.isCategory():
            return False
        for baseClassObject in self.instance.__class__.__bases__:
            if baseClassObject.__name__ == 'VirtualPackageBase': return True
        return False

    def isCategory(self):
        return not self.source

    def isIgnored(self):
        import options
        if not self.path:
            return False
        ignored = options.UserOptions.get(self).ignored
        if ignored is not None:
            return ignored
        ignored = self.path and CraftPackageObject.Ignores.match(self.path)
        if ignored:
            CraftCore.log.warning(f"You are using the deprecated Ignore setting:\n"
                                  f"[Blueprints]\n"
                                  f"Ignores={self.path}\n\n"
                                  f"Please use BlueprintSettings.ini\n"
                                  f"[{self.path}]\n"
                                  f"ignored = True")
        return ignored

    @property
    def version(self):
        if self.isCategory():
            return None
        if not self._version:
            self._version = self.instance.version
        return self._version

    def __eq__(self, other):
        if isinstance(other, CraftPackageObject):
            return self.path == other.path
        return self.path == other

    def __str__(self):
        return self.path or "None"

    def __hash__(self):
        return self.path.__hash__()

    @staticmethod
    def installables():
        #ensure that everything is loaded
        CraftPackageObject.root()
        recipes = []
        for p in CraftPackageObject._recipes.values():
            recipes.extend(p)
        return recipes


class BlueprintException(Exception):
    def __init__(self, message, package, exception=None):
        Exception.__init__(self, message)

        self.package = package
        self.exception = exception

    def __str__(self):
        return f"{self.package.source or self.package} failed: {Exception.__str__(self)}"


class BlueprintNotFoundException(Exception):
    def __init__(self, packageName, message=None):
        Exception.__init__(self)
        self.packageName = packageName
        self.message = message

    def __str__(self):
        if self.message:
            return self.message
        else:
            return f"Failed to find {self.packageName}: {Exception.__str__(self)}"
