#!/usr/bin/env python
import copy
import importlib
import os
import re

from CraftConfig import craftSettings
from CraftStandardDirs import CraftStandardDirs
from CraftDebug import craftDebug
from CraftOS.osutils import OsUtils
import utils


class CraftPackageObject(object):
    options = None
    __rootPackage = None
    _nodes = {}#all nodes
    _recipes = {}#all recipes, for lookup by package name
    IgnoredDirectories = [".git", "__pycache__"]
    Ignores = re.compile("a^")

    def __init__(self, path=None):
        if isinstance(path, CraftPackageObject):
            self.__dict__ = path.__dict__
            return
        if path:
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
                    craftDebug.log.info(f"Found multiple recipes for {path}")
                    for p in packages:
                        craftDebug.log.info(p)
                    craftDebug.log.info(f"Please use the full path to the recipe.")
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
            if package.path in CraftPackageObject._nodes:
                existingNode = CraftPackageObject._nodes[package.path]
                if not existingNode.isCategory():
                    raise BlueprintException(
                        f"Found a recipe clash {existingNode.source} and {blueprintRoot}/{package.path}", existingNode)
                package = existingNode
            else:
                CraftPackageObject._nodes[package.path] = package
        elif blueprintRoot:
            path = blueprintRoot
        else:
            return

        hasChildren = False
        for f in os.listdir(path):
            fPath = os.path.abspath(os.path.join(path, f))
            if os.path.isdir(fPath):
                if f not in CraftPackageObject.IgnoredDirectories:
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
        if hasChildren:
            if package.source:
                raise BlueprintException(f"{package} has has children but also a recipe {package.source}!", package)
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
        if ("Blueprints", "Locations") in craftSettings:
            for path in craftSettings.getList("Blueprints", "Locations"):
                rootDirs.add(utils.normalisePath(path))
        if os.path.isdir(CraftStandardDirs.blueprintRoot()):
            for f in os.listdir(CraftStandardDirs.blueprintRoot()):
                rootDirs.add(utils.normalisePath(os.path.join(CraftStandardDirs.blueprintRoot(), f)))
        return list(rootDirs)


    @staticmethod
    def root():
        if not CraftPackageObject.__rootPackage:
            if ("Blueprints", "Ignores") in craftSettings:
                CraftPackageObject.Ignores = re.compile("|".join([f"^{entry}$" for entry in craftSettings.get("Blueprints", "Ignores").split(";")]))

            CraftPackageObject.__rootPackage = root = CraftPackageObject()
            root.path = "/"
            for blueprintRoot in CraftPackageObject.rootDirectories():
                if not os.path.isdir(blueprintRoot):
                    craftDebug.log.warning(f"{blueprintRoot} does not exist")
                    continue
                blueprintRoot = utils.normalisePath(os.path.abspath(blueprintRoot))
                # create a dummy package to load its children
                child = root._addNode(None, blueprintRoot)
                root.children.update(child.children)
        return CraftPackageObject.__rootPackage


    @property
    def instance(self):
        if not self._instance:
            craftDebug.log.debug(f"module to import: {self.source}")
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


