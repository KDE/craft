from enum import unique, Enum


from CraftDebug import craftDebug
from CraftPackageObject import PackageObjectBase


@unique
class DependencyType(Enum):
    Runtime     = "runtime"
    Buildtime   = "buildtime"
    Both        = "both"


class PortageException(Exception,PackageObjectBase):
    def __init__(self, message, category, package , exception = None):
        Exception.__init__(self, message)
        subpackage, package = PackageObjectBase.PortageInstance.getSubPackage(category,package)
        PackageObjectBase.__init__(self,category,subpackage,package)
        self.exception = exception

    def __hash__(self):
        return self.__str__().__hash__()

    def __str__(self):
        return "%s failed: %s" % (PackageObjectBase.__str__(self),Exception.__str__(self))


class DependencyPackage(PackageObjectBase):
    _packageCache = dict()

    @unique
    class State(Enum):
        Unvisited = 0
        Visiting  = 1
        Visited = 2


    def __init__( self, category, name):
        subpackage, package = PackageObjectBase.PortageInstance.getSubPackage(category,name)
        PackageObjectBase.__init__(self, category, subpackage, package)
        self.runtimeChildren = []
        self.buildChildren = []
        self._version = None
        self.state = DependencyPackage.State.Unvisited


    @staticmethod
    def resolveDependenciesForList(list, depType=DependencyType.Both, maxDepth=-1, ignoredPackages=None):
        dummy = DependencyPackage(None, None)
        if depType == DependencyType.Buildtime:
            dummy.buildChildren = dummy.__readDependenciesForChildren(list)
        else:
            dummy.runtimeChildren = dummy.__readDependenciesForChildren(list)
        out = dummy.getDependencies(depType=depType,maxDepth=maxDepth, ignoredPackages=ignoredPackages)
        # remove the dummy
        del out[-1]
        return out


    @property
    def name(self):
        return self.package

    def __str__(self):
        return f"{PackageObjectBase.__str__(self)}: {self.version}"

    def __resolveDependencies(self):
        craftDebug.log.debug("solving package {self}")
        if self.package:
            subinfo = PackageObjectBase.PortageInstance._getSubinfo(self.category, self.package)
            self.runtimeChildren.extend(self.__readDependenciesForChildren(subinfo.runtimeDependencies.keys()))
            self.buildChildren.extend(self.__readDependenciesForChildren(subinfo.buildDependencies.keys()))

    def __readDependenciesForChildren(self, deps):
        children = []
        if deps:
            for line in deps:
                if line not in DependencyPackage._packageCache:
                    category, package = line.split( "/" )
                    p = DependencyPackage( category, package)
                    craftDebug.log.debug("adding package {line}")
                    DependencyPackage._packageCache[ line ] = p
                    p.__resolveDependencies()
                else:
                    p = DependencyPackage._packageCache[ line ]
                children.append( p )
        return children

    def __getDependencies( self, depType, maxDepth, depth, ignoredPackages ):
        """ returns all dependencies """
        if self.package and PackageObjectBase.PortageInstance.ignores.match(PackageObjectBase.__str__(self)):
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
            if not PackageObjectBase.PortageInstance.ignores.match(p.fullName())\
                    and ( not ignoredPackages or p.fullName() not in ignoredPackages ):
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
