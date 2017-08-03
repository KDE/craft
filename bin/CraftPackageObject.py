#!/usr/bin/env python
import glob
import importlib
import re
from enum import unique, Enum

import os

import builtins

import copy

from CraftConfig import craftSettings, CraftStandardDirs
from CraftDebug import craftDebug

class CraftPackageObject(object):
    options = None
    rootPackage = None
    _packages = None
    _recipes = {}
    IgnoredDirectories = [".git", "__pycache__"]
    Ignores = re.compile("a^")

    def __init__(self, path=None, portageRoot=None, useCache=True):
        self.path = None
        self.children = {}
        self.source = None
        self._version = None
        self._instance = None

        if path:
            self.__getNode(path, portageRoot, useCache)

    def __getNode(self, path, portageRoot, useCache):
        if CraftPackageObject._packages == None:
            CraftPackageObject._packages = {}
            CraftPackageObject.load()

        if isinstance(path, CraftPackageObject):
            self.__dict__ = path.__dict__
            return

        path = path.replace("\\", "/")
        if useCache:
            if path not in CraftPackageObject._packages:
                if path in CraftPackageObject._recipes:
                    package = CraftPackageObject._recipes[path]
                else:
                    package = CraftPackageObject.rootPackage.child(path.split("/"))
            else:
                package = CraftPackageObject._packages[path]

            self.__dict__ = package.__dict__
        else:
            if path == "/":
                self.path = path
                path = portageRoot
            else:
                self.path = path[len(portageRoot) + 1:]
            if portageRoot:
                CraftPackageObject._packages[self.path] = self
            else:
                return

            try:
                hasChildren = False
                for f in os.listdir(path):
                    fPath = os.path.join(path, f)
                    if os.path.isdir(fPath):
                        if f not in CraftPackageObject.IgnoredDirectories:
                            hasChildren = True
                            child = CraftPackageObject(fPath, portageRoot, useCache=False)
                            self.children[child.name] = child
                    elif f.endswith(".py"):
                        if self.source:
                            raise Exception("Multiple py files in one directory")
                        recipe = os.path.splitext(f)[0]
                        if recipe in CraftPackageObject._recipes:
                            raise PortageException(
                                f"Multiple recipes found in {path}, previous recipe is {CraftPackageObject._recipes[recipe]}")
                        CraftPackageObject._recipes[recipe] = self
                        self.source = fPath
                if hasChildren:
                    if self.source:
                        category = copy.deepcopy(self)
                        category.source = None
                    else:
                        category = self
                    self.children["*"] = category
            except Exception as e:
                raise e

    def child(self, paths, pos = 0):
        if paths:
            key = paths[pos]
            if key not in self.children:
                raise Exception(f"{key} is not a child of {self}, path was {'/'.join(paths)}")
            if pos + 1 == len(paths):
                return self.children[key]
            return self.children[key].child(paths, pos + 1)

    @property
    def parent(self):
        """
        Return the parent or the root node if we are a portage
        :return:
        """
        return CraftPackageObject._packages.get(os.path.dirname(self.path), CraftPackageObject._packages[None])

    @property
    def name(self):
        split = self.path.rsplit("/", 1)
        return split[0] if len(split) == 1 else split[1]

    @staticmethod
    def rootDirectories():
        # this function should return all currently set portage directories
        if ("General", "Portages") in craftSettings:
            rootDirs = craftSettings.get("General", "Portages").split(";")
        if not rootDirs:
            rootDirs = [CraftStandardDirs.craftRepositoryDir()]
        return rootDirs


    @staticmethod
    def load():
        if not CraftPackageObject.rootPackage:
            if ("Portage", "Ignores") in craftSettings:
                CraftPackageObject.Ignores = re.compile("|".join([f"^{entry}$" for entry in craftSettings.get("Portage", "Ignores").split(";")]))

            CraftPackageObject.rootPackage = CraftPackageObject("/", None, useCache=False)
            for portage in CraftPackageObject.rootDirectories():
                portage = portage.replace("\\", "/")
                children = CraftPackageObject("/", portage, useCache=False).children
                CraftPackageObject.rootPackage.children.update(children)
        return CraftPackageObject.rootPackage


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
            self._version = self.subinfo.defaultTarget
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
        CraftPackageObject.load()
        return CraftPackageObject._recipes.values()


@unique
class DependencyType(Enum):
    Runtime = "runtime"
    Buildtime = "buildtime"
    Both = "both"


class PortageException(Exception, CraftPackageObject):
    def __init__(self, message, package, exception=None):
        Exception.__init__(self, message)
        CraftPackageObject.__init__(self, package.path)
        self.exception = exception

    def __str__(self):
        return "%s failed: %s" % (CraftPackageObject.__str__(self), Exception.__str__(self))


class DependencyPackage(CraftPackageObject):
    _packageCache = dict()

    @unique
    class State(Enum):
        Unvisited = 0
        Visiting = 1
        Visited = 2

    def __init__(self, path):
        CraftPackageObject.__init__(self, path)
        self._depenendencyType = None
        self.runtimeChildren = []
        self.dependencies = []
        self.state = DependencyPackage.State.Unvisited


    @property
    def depenendencyType(self):
        return self._depenendencyType

    @depenendencyType.setter
    def depenendencyType(self, depenendencyType):
        if self._depenendencyType != depenendencyType:
            self._depenendencyType = depenendencyType
            self.dependencies = []
            self.__resolveDependencies()

    def __resolveDependencies(self):
        craftDebug.log.debug(f"solving package {self}")
        if not self.isCategory():
            subinfo = self.subinfo
            if self.depenendencyType in [DependencyType.Both, DependencyType.Runtime]:
                self.dependencies.extend(self.__readDependenciesForChildren(subinfo.runtimeDependencies.keys()))
            if self.depenendencyType in [DependencyType.Both, DependencyType.Buildtime]:
                self.dependencies.extend(self.__readDependenciesForChildren(subinfo.buildDependencies.keys()))
        else:
            self.dependencies.extend(self.__readDependenciesForChildren(self.children.values()))

    def __readDependenciesForChildren(self, deps):
        children = []
        if deps:
            for line in deps:
                if line not in DependencyPackage._packageCache:
                    p = DependencyPackage(line)
                    craftDebug.log.debug(f"adding package {line}")
                    DependencyPackage._packageCache[line] = p
                else:
                    p = DependencyPackage._packageCache[line]
                p.depenendencyType = self.depenendencyType
                children.append(p)
        return children

    def __getDependencies(self, depenendencyType, maxDepth, depth, ignoredPackages):
        """ returns all dependencies """
        if self.isIgnored():
            return []

        depList = []

        self.state = DependencyPackage.State.Visiting
        for p in self.dependencies:
            if p.state != DependencyPackage.State.Unvisited:
                continue
            if not p.isIgnored() \
                    and (not ignoredPackages or p.path not in ignoredPackages):
                if maxDepth == -1 or depth < maxDepth:
                    depList.extend(p.__getDependencies(depenendencyType, maxDepth, depth + 1, ignoredPackages))

        if self.state != DependencyPackage.State.Visited:
            self.state = DependencyPackage.State.Visited
            if not self.isCategory():
                depList.append(self)
        return depList

    def getDependencies(self, depType=DependencyType.Both, maxDepth=-1, ignoredPackages=None):
        self.depenendencyType = depType
        for p in DependencyPackage._packageCache.values():
            #reset visited state
            p.state = DependencyPackage.State.Unvisited
        return self.__getDependencies(depType, maxDepth, 0, ignoredPackages)
