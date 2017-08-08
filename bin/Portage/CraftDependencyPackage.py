from enum import unique, Enum

from CraftDebug import craftDebug
from Portage.CraftPackageObject import CraftPackageObject


@unique
class DependencyType(Enum):
    Runtime = "runtime"
    Buildtime = "buildtime"
    Both = "both"


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
                    p = DependencyPackage(CraftPackageObject.get(line))
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
