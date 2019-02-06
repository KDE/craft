from collections import OrderedDict
from enum import unique, Enum, IntFlag

from Blueprints.CraftPackageObject import CraftPackageObject, BlueprintException
from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore
from Package import VirtualPackageBase
from info import DependencyRequirementType


@unique
class DependencyType(IntFlag):
    Runtime     = 0x1 << 0
    Buildtime   = 0x1 << 1
    # TODO: rename as we now have more build types
    Both        = Runtime | Buildtime
    Packaging   = 0x1 << 3

    All         = ~0


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
        CraftCore.log.debug(f"resolving package {self}")
        if not self.isCategory():
            subinfo = self.subinfo
            if self.depenendencyType & DependencyType.Runtime:
                self.dependencies.extend(self.__readDependenciesForChildren(subinfo.runtimeDependencies.items()))
            if self.depenendencyType & DependencyType.Buildtime:
                self.dependencies.extend(self.__readDependenciesForChildren(subinfo.buildDependencies.items()))
            if self.depenendencyType & DependencyType.Packaging:
                self.dependencies.extend(self.__readDependenciesForChildren(subinfo.packagingDependencies.items()))
        else:
            self.dependencies.extend(self.__readDependenciesForChildren([(x, None) for x in self.children.values()]))

    def __readDependenciesForChildren(self, deps : [(str, str)]) -> []:
        children = []
        if deps:
            for packaheName, requiredVersion in deps:
                if (packaheName, self.depenendencyType) not in CraftDependencyPackage._packageCache:
                    package = CraftPackageObject.get(packaheName)
                    if not package:
                        raise BlueprintException(f"Failed to resolve {packaheName} as a dependency of {self}", self)
                    if isinstance(requiredVersion, tuple):
                        requiredVersion, type = requiredVersion
                        if type == DependencyRequirementType.Required:
                            if not bool(package.categoryInfo.compiler & CraftCore.compiler.compiler):
                                raise BlueprintException(f"{self} requries {package}, but it is not supported on {CraftCore.compiler.compiler}",self)
                            if not bool(package.categoryInfo.platforms & CraftCore.compiler.platform):
                                raise BlueprintException(f"{self} requries {package}, but it is not supported on {CraftCore.compiler.platform}",self)
                            if package.isIgnored() or isinstance(package.instance, VirtualPackageBase.VirtualPackageBase):
                                raise BlueprintException(f"{self} requries {package}, but it is ignored",self)

                    if requiredVersion and requiredVersion != None and CraftVersion(package.version) < CraftVersion(requiredVersion):
                        raise BlueprintException(f"{self} requries {package} version {requiredVersion!r} but {package.version!r} is installed", self)

                    p = CraftDependencyPackage(package)
                    CraftCore.log.debug(f"adding package {packaheName}")
                    CraftDependencyPackage._packageCache[(packaheName, self.depenendencyType)] = p
                    p.depenendencyType = self.depenendencyType
                else:
                    p = CraftDependencyPackage._packageCache[(packaheName, self.depenendencyType)]
                children.append(p)
        return children

    def __getDependencies(self, depenendencyType, ignoredPackages):
        """ returns all dependencies """
        if self.isIgnored():
            return []
        self.depenendencyType = depenendencyType

        depList = []

        self.state = CraftDependencyPackage.State.Visiting
        for p in self.dependencies:
            if p.state != CraftDependencyPackage.State.Unvisited:
                continue
            if not p.isIgnored() \
                    and (not ignoredPackages or p.path not in ignoredPackages):
                depList.extend(p.__getDependencies(depenendencyType & ~DependencyType.Packaging, ignoredPackages))
                if depenendencyType & DependencyType.Packaging:
                    depList.extend(p.__getDependencies(depenendencyType, ignoredPackages))

        if self.state != CraftDependencyPackage.State.Visited:
            self.state = CraftDependencyPackage.State.Visited
            if not self.isCategory():
                depList.append(self)
        return list(OrderedDict.fromkeys(depList))

    def getDependencies(self, depType=DependencyType.All, ignoredPackages=None):
        self.depenendencyType = depType
        for p in CraftDependencyPackage._packageCache.values():
            #reset visited state
            p.state = CraftDependencyPackage.State.Unvisited
        return self.__getDependencies(depType, ignoredPackages)
