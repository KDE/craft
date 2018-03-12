from enum import unique, Enum

from CraftCore import CraftCore
from Blueprints.CraftPackageObject import CraftPackageObject, BlueprintException
from Blueprints.CraftVersion import CraftVersion


@unique
class DependencyType(Enum):
    Runtime = 0
    Buildtime = 1
    Both = 2


class CraftDependencyPackage(CraftPackageObject):
    _packageCache = dict()

    @unique
    class State(Enum):
        Unvisited = 0
        Visiting = 1
        Visited = 2

    def __init__(self, path):
        CraftPackageObject.__init__(self, path)
        self._depenendencyType = None
        self.dependencies = [] # tuple (name, required version)
        self.state = CraftDependencyPackage.State.Unvisited


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
        CraftCore.log.debug(f"solving package {self}")
        if not self.isCategory():
            subinfo = self.subinfo
            if self.depenendencyType in [DependencyType.Both, DependencyType.Runtime]:
                self.dependencies.extend(self.__readDependenciesForChildren(subinfo.runtimeDependencies.items()))
            if self.depenendencyType in [DependencyType.Both, DependencyType.Buildtime]:
                self.dependencies.extend(self.__readDependenciesForChildren(subinfo.buildDependencies.items()))
        else:
            self.dependencies.extend(self.__readDependenciesForChildren([(x, None) for x in self.children.values()]))

    def __readDependenciesForChildren(self, deps):
        children = []
        if deps:
            for packaheName, requiredVersion in deps:
                if packaheName not in CraftDependencyPackage._packageCache:
                    package = CraftPackageObject.get(packaheName)
                    if not package:
                        raise BlueprintException(f"Failed to resolve {packaheName} as a dependency of {self}", self)
                    if requiredVersion and requiredVersion != "default" and CraftVersion(package.version) < CraftVersion(requiredVersion):
                        raise BlueprintException(f"{self} requries {package} version {requiredVersion!r} but {package.version!r} is installed", self)

                    p = CraftDependencyPackage(package)
                    CraftCore.log.debug(f"adding package {packaheName}")
                    CraftDependencyPackage._packageCache[packaheName] = p
                else:
                    p = CraftDependencyPackage._packageCache[packaheName]
                p.depenendencyType = self.depenendencyType
                children.append(p)
        return children

    def __getDependencies(self, depenendencyType, ignoredPackages):
        """ returns all dependencies """
        if self.isIgnored():
            return []

        depList = []

        self.state = CraftDependencyPackage.State.Visiting
        for p in self.dependencies:
            if p.state != CraftDependencyPackage.State.Unvisited:
                continue
            if not p.isIgnored() \
                    and (not ignoredPackages or p.path not in ignoredPackages):
                depList.extend(p.__getDependencies(depenendencyType, ignoredPackages))

        if self.state != CraftDependencyPackage.State.Visited:
            self.state = CraftDependencyPackage.State.Visited
            if not self.isCategory():
                depList.append(self)
        return depList

    def getDependencies(self, depType=DependencyType.Both, ignoredPackages=None):
        self.depenendencyType = depType
        for p in CraftDependencyPackage._packageCache.values():
            #reset visited state
            p.state = CraftDependencyPackage.State.Unvisited
        return self.__getDependencies(depType, ignoredPackages)
