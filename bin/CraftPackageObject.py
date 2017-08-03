#!/usr/bin/env python
import glob
import importlib
import re
from enum import unique, Enum

import os

import builtins

from CraftConfig import craftSettings, CraftStandardDirs
from CraftDebug import craftDebug

class PackageObjectBase(object):
    options = None
    rootPackage = None
    _packages = None
    _recipes = {}
    IgnoredDirectories = [".git", "__pycache__"]
    Ignores = re.compile("a^")

    def __init__(self, path, portageRoot=None, useCache=True):
        if PackageObjectBase._packages == None:
            PackageObjectBase._packages = {}
            PackageObjectBase.load()
        self.path = None

        self.children = []
        self.source = None
        self._version = None
        self._instance = None

        if isinstance(path, PackageObjectBase):
            self.__dict__ = path.__dict__
            return

        path = path.replace("\\", "/")
        if useCache:
            # TODO: a real package resoulution
            package = None
            if path not in PackageObjectBase._packages:
                for p in PackageObjectBase._packages.values():
                    split = p.path.rsplit("/", 1)
                    if len(split) > 1:
                        cat, pack = split
                        if path in cat or path == pack:
                            package = p
                            break
                    else:
                        if path in path:
                            package = p
                            continue
            else:
                package = PackageObjectBase._packages[path]
            #print(path, package)
            self.__dict__ = package.__dict__
        else:
            if path == "/":
                self.path = path
                path = portageRoot
            else:
                self.path = path[len(portageRoot) + 1:]
            if portageRoot:
                PackageObjectBase._packages[self.path] = self

            try:
                for f in os.listdir(path):
                    fPath = os.path.join(path, f)
                    if os.path.isdir(fPath):
                        if f not in PackageObjectBase.IgnoredDirectories:
                            self.children.append(PackageObjectBase(fPath, portageRoot, useCache=False))
                    elif f.endswith(".py"):
                        if self.source:
                            raise Exception("Multiple py files in one directory")
                        PackageObjectBase._recipes[fPath] = self
                        self.source = fPath
            except Exception:
                pass

    @property
    def parent(self):
        """
        Return the parent or the root node if we are a portage
        :return:
        """
        return PackageObjectBase._packages.get(os.path.dirname(self.path), PackageObjectBase._packages[None])

    @property
    def name(self):
        return self.path.rsplit("/", 1)[1]

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
        if not PackageObjectBase.rootPackage:
            if ("Portage", "Ignores") in craftSettings:
                PackageObjectBase.Ignores = re.compile("|".join([f"^{entry}$" for entry in craftSettings.get("Portage", "Ignores").split(";")]))

            PackageObjectBase.rootPackage = PackageObjectBase("/", None, useCache=False)
            for portage in PackageObjectBase.rootDirectories():
                portage = portage.replace("\\", "/")
                PackageObjectBase.rootPackage.children.extend(PackageObjectBase("/", portage, useCache=False).children)
        return PackageObjectBase.rootPackage


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
        for baseClassObject in self.instance.__class__.__bases__:
            if baseClassObject.__name__ == 'VirtualPackageBase': return True
        return False

    def isCategory(self):
        return not self.source

    def isIgnored(self):
        return not self.path or PackageObjectBase.Ignores.match(self.path)

    @property
    def version(self):
        if not self._version:
            self._version = self.subinfo.defaultTarget
        return self._version

    def __eq__(self, other):
        if isinstance(other, PackageObjectBase):
            return self.path == other.path
        return self.path == other

    def __str__(self):
        return self.path

    def __hash__(self):
        return self.path.__hash__()

    @staticmethod
    def installables():
        PackageObjectBase.load()
        print("\n".join([ str(x) for x in PackageObjectBase._recipes.values()]))
        return PackageObjectBase._recipes.values()


@unique
class DependencyType(Enum):
    Runtime = "runtime"
    Buildtime = "buildtime"
    Both = "both"


class PortageException(Exception, PackageObjectBase):
    def __init__(self, message, package, exception=None):
        Exception.__init__(self, message)
        PackageObjectBase.__init__(self, package.path)
        self.exception = exception

    def __str__(self):
        return "%s failed: %s" % (PackageObjectBase.__str__(self), Exception.__str__(self))


class DependencyPackage(PackageObjectBase):
    _packageCache = dict()

    @unique
    class State(Enum):
        Unvisited = 0
        Visiting = 1
        Visited = 2

    def __init__(self, path):
        PackageObjectBase.__init__(self, path)
        self.runtimeChildren = []
        self.buildChildren = []
        self.state = DependencyPackage.State.Unvisited

    def __resolveDependencies(self):
        craftDebug.log.debug(f"solving package {self}")
        if self.path != "null":
            subinfo = self.subinfo
            self.runtimeChildren.extend(self.__readDependenciesForChildren(subinfo.runtimeDependencies.keys()))
            self.buildChildren.extend(self.__readDependenciesForChildren(subinfo.buildDependencies.keys()))

    def __readDependenciesForChildren(self, deps):
        children = []
        if deps:
            for line in deps:
                if line not in DependencyPackage._packageCache:
                    p = DependencyPackage(line)
                    craftDebug.log.debug(f"adding package {line}")
                    DependencyPackage._packageCache[line] = p
                    p.__resolveDependencies()
                else:
                    p = DependencyPackage._packageCache[line]
                children.append(p)
        return children

    def __getDependencies(self, depType, maxDepth, depth, ignoredPackages):
        """ returns all dependencies """
        if self.isIgnored():
            return []

        depList = []

        if depType == DependencyType.Runtime:
            children = self.runtimeChildren
        elif depType == DependencyType.Buildtime:
            children = self.buildChildren
        else:
            children = self.runtimeChildren + self.buildChildren

        self.state = DependencyPackage.State.Visiting
        for p in children:
            if p.state != DependencyPackage.State.Unvisited:
                continue
            if not p.isIgnored() \
                    and (not ignoredPackages or p.fullName() not in ignoredPackages):
                if maxDepth == -1 or depth < maxDepth:
                    depList.extend(p.__getDependencies(depType, maxDepth, depth + 1, ignoredPackages))

        if self.state != DependencyPackage.State.Visited:
            self.state = DependencyPackage.State.Visited
            depList.append(self)
        return depList

    def getDependencies(self, depType=DependencyType.Both, maxDepth=-1, ignoredPackages=None):
        self.__resolveDependencies()
        for p in DependencyPackage._packageCache.values():
            p.state = DependencyPackage.State.Unvisited
        return self.__getDependencies(depType, maxDepth, 0, ignoredPackages)
