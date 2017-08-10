from enum import unique, Enum

from CraftDebug import craftDebug
from Portage.CraftPackageObject import CraftPackageObject


@unique
class DependencyType(Enum):
    Runtime = "runtime"
    Buildtime = "buildtime"
    Both = "both"


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
        self.runtimeChildren = []
        self.dependencies = []
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
                if line not in CraftDependencyPackage._packageCache:
                    p = CraftDependencyPackage(CraftPackageObject.get(line))
                    craftDebug.log.debug(f"adding package {line}")
                    CraftDependencyPackage._packageCache[line] = p
                else:
                    p = CraftDependencyPackage._packageCache[line]
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
