#!/usr/bin/env python
import copy
import importlib
import os
import re

from CraftConfig import craftSettings, CraftStandardDirs
from CraftDebug import craftDebug
from CraftOS.osutils import OsUtils


class CraftPackageObject(object):
    options = None
    __rootPackage = None
    _nodes = {}#all nodes
    _recipes = {}#all recipes, for lookup by package name
    IgnoredDirectories = [".git", "__pycache__"]
    Ignores = re.compile("a^")

    def __init__(self, path):
        if isinstance(path, CraftPackageObject):
            self.__dict__ = path.__dict__
            return
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

    def _addNode(self, path, portageRoot):
        package = CraftPackageObject(path)
        if path:
            if OsUtils.isWin():
                path = path.replace("\\", "/")
            package.path = path[len(portageRoot) + 1:]
            if package.path in CraftPackageObject._nodes:
                return
            CraftPackageObject._nodes[package.path] = package
        elif portageRoot:
            path = portageRoot
        else:
            return

        hasChildren = False
        for f in os.listdir(path):
            fPath = os.path.abspath(os.path.join(path, f))
            if os.path.isdir(fPath):
                if f not in CraftPackageObject.IgnoredDirectories:
                    hasChildren = True
                    child = self._addNode(fPath, portageRoot)
                    if child:
                        package.children[child.name] = child
            elif f.endswith(".py"):
                if package.source:
                    raise Exception("Multiple py files in one directory")
                recipe = os.path.splitext(f)[0]
                if recipe not in CraftPackageObject._recipes:
                    CraftPackageObject._recipes[recipe] = []
                CraftPackageObject._recipes[recipe].append(package)
                package.source = fPath
        if hasChildren:
            if package.source:
                raise PortageException(f"{package} has has children but also a recipe {package.source}!")
        return package

    @property
    def name(self):
        if not self.path:
            return "[]"
        split = self.path.rsplit("/", 1)
        return split[0] if len(split) == 1 else split[1]

    @staticmethod
    def rootDirectories():
        # this function should return all currently set portage directories
        rootDirs = None
        if ("General", "Portages") in craftSettings:
            rootDirs = craftSettings.getList("General", "Portages")
        if not rootDirs:
            rootDirs = [CraftStandardDirs.craftRepositoryDir()]
        return rootDirs


    @staticmethod
    def root():
        if not CraftPackageObject.__rootPackage:
            if ("Portage", "Ignores") in craftSettings:
                CraftPackageObject.Ignores = re.compile("|".join([f"^{entry}$" for entry in craftSettings.get("Portage", "Ignores").split(";")]))

            CraftPackageObject.__rootPackage = root = CraftPackageObject("/")
            for portage in CraftPackageObject.rootDirectories():
                if OsUtils.isWin():
                    portage = os.path.abspath(portage).replace("\\", "/")
                # create a dummy package to load its children
                child = root._addNode(None, portage)
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
                raise PortageException(f"Failed to load file {self.source}", self, e)
            if not mod is None:
                mod.CRAFT_CURRENT_MODULE = self
                pack = mod.Package()
                self._instance = pack
            else:
                raise PortageException("Failed to find package", self)
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
        return CraftPackageObject._recipes.values()


class PortageException(Exception, CraftPackageObject):
    def __init__(self, message, package, exception=None):
        Exception.__init__(self, message)
        CraftPackageObject.__init__(self, package.path)
        self.exception = exception

    def __str__(self):
        return "%s failed: %s" % (CraftPackageObject.__str__(self), Exception.__str__(self))


