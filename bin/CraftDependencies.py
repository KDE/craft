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
    """ This class wraps each package and constructs the dependency tree
        original code is from dependencies.py, integration will come later...
        """

    def __init__( self, category, name, autoExpand = True, parent = None ):
        subpackage, package = PackageObjectBase.PortageInstance.getSubPackage(category,name)
        PackageObjectBase.__init__(self, category, subpackage, package)
        self.runtimeChildren = []
        self.buildChildren = []
        self._version = None
        if parent is None:
            self._dependencyList = dict()
        else:
            self._dependencyList = parent._dependencyList

        if autoExpand:
            self.__readChildren()

    @property
    def name(self):
        return self.package


    def __hash__(self):
        return self.__str__().__hash__()

    def __eq__( self, other ):
        return self.category == other.category and self.name == other.name

    def __ne__( self, other ):
        return self.category != other.category or self.name != other.name

    def __str__(self):
        return f"{PackageObjectBase.__str__(self)}: {self.version}"

    def __readChildren( self ):
        runtimeDependencies, buildDependencies = self._readChildren(self.category, self.name)
        self.runtimeChildren = self.__readDependenciesForChildren( list(runtimeDependencies.keys()) )
        self.buildChildren = self.__readDependenciesForChildren( list(buildDependencies.keys()) )

    def __readDependenciesForChildren( self, deps):
        children = []
        if deps:
            for line in deps:
                ( category, package ) = line.split( "/" )
                if not line in self._dependencyList.keys():
                    p = DependencyPackage( category, package, False, self )
                    craftDebug.log.debug("adding package {line}")
                    self._dependencyList[ line ] = p
                    p.__readChildren()
                else:
                    p = self._dependencyList[ line ]
                children.append( p )
        return children

    def getDependencies( self, depList = None, depType=DependencyType.Both, single = set(), maxDepth = -1, depth = 0, ignoredPackages = None):
        """ returns all dependencies """
        if depList is None:
            depList = []
        if depType == DependencyType.Runtime:
            children = self.runtimeChildren
        elif depType == DependencyType.Buildtime:
            children = self.buildChildren
        else:
            children = self.runtimeChildren + self.buildChildren

        single.add(self)
        for p in children:
            if not p in single and not p in depList\
                    and not PackageObjectBase.PortageInstance.ignores.match(p.fullName())\
                    and not p.fullName() in (ignoredPackages or []):
                if maxDepth == -1:
                    p.getDependencies( depList, depType, single )
                elif depth < maxDepth:
                    p.getDependencies( depList, depType, single, maxDepth = maxDepth, depth = depth + 1 )

        #if self.category != internalCategory:
        if not self in depList and not PackageObjectBase.PortageInstance.ignores.match(PackageObjectBase.__str__(self)):
            depList.append( self )

        return depList
