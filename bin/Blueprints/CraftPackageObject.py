#!/usr/bin/env python
import copy
import importlib
import os
import re

import CraftConfig
from CraftStandardDirs import CraftStandardDirs
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
import utils


class CraftPackageObject(object):
    options = None
    __rootPackage = None
    _nodes = {}#all nodes
    _recipes = {}#all recipes, for lookup by package name
    IgnoredDirectories = ["__pycache__"]
    Ignores = re.compile("a^")

    def __init__(self, other=None):
        if isinstance(other, CraftPackageObject):
            self.__dict__ = other.__dict__
            return
        if other:
            raise Exception("Calling CraftPackageObject(str) directly is not supported,"
                            " use CraftPackageObject.get(str) instead.")

        self.path = None
        self.children = {}
        self.source = None
        self._version = None
        self._instance = None

    @property
    def parentPath(self):
        if not self.path:
            return []
        split = self.path.rsplit("/", 1)
        return split[1] if len(split)>1 else "/"

    @property
    def parent(self):
        if not self.path:
            return "/"
        return CraftPackageObject._nodes[self.parentPath]

    @staticmethod
    def get(path):
        if isinstance(path, CraftPackageObject):
            return path
        CraftPackageObject.root()
        package = None
        if path not in CraftPackageObject._nodes:
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
            package = CraftPackageObject._nodes[path]
        return package

    def _addNode(self, path, blueprintRoot):
        package = CraftPackageObject()
        if path:
            path = utils.normalisePath(path)
            package.path = path[len(blueprintRoot) + 1:]
        elif blueprintRoot:
            path = blueprintRoot
        else:
            return None

        for f in os.listdir(path):
            fPath = os.path.abspath(os.path.join(path, f))
            if os.path.isdir(fPath):
                if not f.startswith(".") and f not in CraftPackageObject.IgnoredDirectories:
                    hasChildren = True
                    child = self._addNode(fPath, blueprintRoot)
                    if child:
                        package.children[child.name] = child
            elif f.endswith(".py"):
                if package.source:
                    raise BlueprintException(f"Multiple py files in one directory: {package.source} and {f}", package)
                if f[:-3] != package.name:
                    raise BlueprintException(f"Recipes must match the name of the directory: {fPath}", package)
                recipe = os.path.splitext(f)[0]
                if recipe not in CraftPackageObject._recipes:
                    CraftPackageObject._recipes[recipe] = []
                CraftPackageObject._recipes[recipe].append(package)
                package.source = fPath
        if package.children:
            if package.source:
                raise BlueprintException(f"{package} has has children but also a recipe {package.source}!", package)


        if path != blueprintRoot:
            if not package.source and not package.children:
                CraftCore.log.warning(f"Found an dead branch in {blueprintRoot}/{package.path}\n"
                                       f"You might wan't to run \"git clean -xdf\" in that directry.")
                return None
            if package.path in CraftPackageObject._nodes:
                existingNode = CraftPackageObject._nodes[package.path]
                if not existingNode.isCategory():
                    raise BlueprintException(
                        f"Found a recipe clash {existingNode.source} and {blueprintRoot}/{package.path}", existingNode)
                existingNode.children.update(package.children)
                package = existingNode
            else:
                CraftCore.log.debug(f"Adding package {package} from {blueprintRoot}")
                CraftPackageObject._nodes[package.path] = package
        return package

    @property
    def name(self):
        if not self.path:
            return "[]"
        split = self.path.rsplit("/", 1)
        return split[0] if len(split) == 1 else split[1]

    @staticmethod
    def rootDirectories():
        # this function should return all currently set blueprint directories
        rootDirs = {utils.normalisePath(CraftStandardDirs.craftRepositoryDir())}
        if ("Blueprints", "Locations") in CraftCore.settings:
            for path in CraftCore.settings.getList("Blueprints", "Locations"):
                rootDirs.add(utils.normalisePath(path))
        if os.path.isdir(CraftStandardDirs.blueprintRoot()):
            for f in os.listdir(CraftStandardDirs.blueprintRoot()):
                rootDirs.add(utils.normalisePath(os.path.join(CraftStandardDirs.blueprintRoot(), f)))
        CraftCore.log.debug(f"Craft BlueprintLocations: {rootDirs}")
        return list(rootDirs)


    @staticmethod
    def root():
        if not CraftPackageObject.__rootPackage:
            if ("Blueprints", "Ignores") in CraftCore.settings:
                CraftPackageObject.Ignores = re.compile("|".join([f"^{entry}$" for entry in CraftCore.settings.get("Blueprints", "Ignores").split(";")]))

            CraftPackageObject.__rootPackage = root = CraftPackageObject()
            root.path = "/"
            for blueprintRoot in CraftPackageObject.rootDirectories():
                if not os.path.isdir(blueprintRoot):
                    CraftCore.log.warning(f"{blueprintRoot} does not exist")
                    continue
                blueprintRoot = utils.normalisePath(os.path.abspath(blueprintRoot))
                # create a dummy package to load its children
                child = root._addNode(None, blueprintRoot)
                root.children.update(child.children)
        return CraftPackageObject.__rootPackage


    @property
    def instance(self):
        if not self._instance:
            CraftCore.log.debug(f"module to import: {self.source}")
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
        return CraftCore.installdb.getInstalledPackages(self.package) is not None

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
        return self.path and CraftPackageObject.Ignores.match(self.path)

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


class BlueprintException(Exception, CraftPackageObject):
    def __init__(self, message, package, exception=None):
        Exception.__init__(self, message)
        CraftPackageObject.__init__(self, package)
        self.exception = exception

    def __str__(self):
        return "%s failed: %s" % (CraftPackageObject.__str__(self), Exception.__str__(self))


