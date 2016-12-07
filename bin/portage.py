## @package portage
#  @brief contains portage tree related functions
#  @note this file should replace all other related portage related files
import builtins
from enum import Enum
import importlib
from collections import OrderedDict

from CraftDebug import craftDebug
from CraftPackageObject import PackageObjectBase
from CraftConfig import *
import InstallDB
import utils

class DependencyType(Enum):
    Runtime     = "runtime"
    Buildtime   = "buildtime"
    Both        = "both"

class PortageCache(object):
    _rootDirCache = dict()

class PortageException(Exception,PackageObjectBase):
    def __init__(self, message, category, package , exception = None):
        Exception.__init__(self, message)
        subpackage, package = getSubPackage(category,package)
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
        subpackage, package = getSubPackage(category,name)
        PackageObjectBase.__init__(self,category,subpackage,package,version = PortageInstance.getDefaultTarget(category,package))
        self.category = category
        self.runtimeChildren = []
        self.buildChildren = []
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
        return "%s: %s" % (PackageObjectBase.__str__(self), self.version)

    def __readChildren( self ):
        runtimeDependencies, buildDependencies = readChildren( self.category, self.name )
        self.runtimeChildren = self.__readDependenciesForChildren( list(runtimeDependencies.keys()) )
        self.buildChildren = self.__readDependenciesForChildren( list(buildDependencies.keys()) )

    def __readDependenciesForChildren( self, deps):
        children = []
        if deps:
            for line in deps:
                ( category, package ) = line.split( "/" )
                craftDebug.log.debug("category: %s, name: %s" % (category, package))
                try:
                    version = PortageInstance.getNewestVersion( category, package )
                except PortageException as e:
                    craftDebug.log.warning("%s for %s/%s as a dependency of %s/%s" % (e, e.category, e.package, self.category , self.name))
                    continue

                if not line in self._dependencyList.keys():
                    p = DependencyPackage( category, package, False, self )
                    craftDebug.log.debug("adding package %s/%s-%s" % (category, package, version))
                    self._dependencyList[ line ] = p
                    p.__readChildren()
                else:
                    p = self._dependencyList[ line ]
                children.append( p )
        return children

    def getDependencies( self, depList = [], depType=DependencyType.Both, single = set(), maxDepth = -1, depth = 0, ignoredPackages = None):
        """ returns all dependencies """
        if depType == DependencyType.Runtime:
            children = self.runtimeChildren
        elif depType == DependencyType.Buildtime:
            children = self.buildChildren
        else:
            children = self.runtimeChildren + self.buildChildren

        single.add(self)
        for p in children:
            if not p in single and not p in depList\
                    and not PortageInstance.ignores.match(p.fullName())\
                    and not p.fullName() in (ignoredPackages or []):
                if maxDepth == -1:
                    p.getDependencies( depList, depType, single )
                elif depth < maxDepth:
                    p.getDependencies( depList, depType, single, maxDepth = maxDepth, depth = depth + 1 )
                    
        #if self.category != internalCategory:
        if not self in depList and not PortageInstance.ignores.match(PackageObjectBase.__str__(self)):
            depList.append( self )

        return depList

def buildType():
    """return currently selected build type"""
    return craftSettings.get("Compile","BuildType")

def rootDirectories():
    # this function should return all currently set portage directories
    if ("General", "EMERGE_PORTAGE_ROOT" ) in craftSettings:
        rootDirs = craftSettings.get("General", "EMERGE_PORTAGE_ROOT" ).split( ";" )
    else:
        rootDirs = []
    if len( rootDirs ) == 0:
        rootDirs = [ CraftStandardDirs.craftRepositoryDir() ]
    return rootDirs

def rootDirForCategory( category ):
    """this function should return the portage directory where it finds the first occurance of the category

throws exception if not found
"""
    # this function should return the portage directory where it finds the
    # first occurance of a category or the default value
    for i in rootDirectories():
        if category and os.path.exists( os.path.join( i, category ) ):
            return i
    craftDebug.log.critical("can't find category %s" % category)

def rootDirForPackage( category, package ):
    """returns the portage directory where it finds the first occurance of this package
"""
    name = "%s/%s" % ( category, package )
    if not name in PortageCache._rootDirCache:
        for i in rootDirectories():
            if os.path.exists( os.path.join( i, category, package ) ):
                PortageCache._rootDirCache[ name ] = i
    return PortageCache._rootDirCache[ name ]

def getFullPackage( package ):
    """tries to find a package and returns either category / subpackage / package or category / package

returns an empty list if not found
"""
    category = PortageInstance.getCategory( package )
    if not category: return []
    if package in PortageInstance.subpackages:
        _cat, subpackage = PortageInstance.subpackages[ package ][0].split('/')
        if not _cat == category: return []
        return [category, subpackage, package]
    else:
        return [category, package]


def getDirname( category, package ):
    """ return absolute pathname for a given category and package """
    subpackage, package = getSubPackage( category, package )
    if category and package:
        if subpackage:
            return os.path.join( rootDirForPackage( category, subpackage ), category, subpackage, package )
        else:
            return os.path.join( rootDirForPackage( category, package ), category, package )
    else:
        craftDebug.log.critical("broken category or package %s/%s" % (category, package))

def getFilename( category, package ):
    """ return absolute filename for a given category, package  """
    return os.path.join( getDirname( category, package ), "%s.py" % package  )

def VCSDirs():
    return [ '.svn', 'CVS', '.hg', '.git' ]

class Portage(object):
    #cache for pacages
    _packageDict = OrderedDict()
    options = ""

    def __init__( self ):
        """ """
        self.categories = {}
        self.subpackages = {}
        self.portages = {}
        self._CURRENT_MODULE = ()#todo refactor package constructor
        self.ignores = re.compile("a^")
        if ("Portage", "Ignores") in craftSettings:
            self.ignores = Portage.generateIgnoreList(craftSettings.get("Portage", "Ignores").split(";"))

    @staticmethod
    def generateIgnoreList(ignores):
        return re.compile("(%s)" % "|".join( ["^%s$" % entry for entry in ignores]))

    def addPortageDir( self, directory ):
        """ adds the categories and packages of a portage directory """
        if not os.path.exists( directory ):
            return

        categoryList = os.listdir( directory )

        # remove vcs directories
        for vcsdir in VCSDirs():
            if vcsdir in categoryList:
                categoryList.remove( vcsdir )
        if "__pycache__" in categoryList:
            categoryList.remove( "__pycache__" )

        dontBuildCategoryList = self.getDontBuildPackagesList( os.path.join( directory ) )

        self.portages[ directory ] = []
        for category in categoryList:
            if not os.path.isdir( os.path.join( directory, category ) ):
                continue

            self.portages[ directory ].append( category )

            packageList = os.listdir( os.path.join( directory, category ) )

            # remove vcs directories
            for vcsdir in VCSDirs():
                if vcsdir in packageList:
                    packageList.remove( vcsdir )
            if "__pycache__" in packageList:
                packageList.remove( "__pycache__" )

            dontBuildPackageList = self.getDontBuildPackagesList( os.path.join( directory, category ) )

            if not category in list(self.categories.keys()):
                self.categories[ category ] = []

            for package in packageList:
                if not os.path.isdir( os.path.join( directory, category, package ) ):
                    continue
                if not package in self.categories[ category ]:
                    _enabled = not category in dontBuildCategoryList and not package in dontBuildPackageList
                    self.categories[ category ].append( PackageObjectBase( category=category, package=package, enabled=_enabled ) )

                subPackageList = os.listdir( os.path.join( directory, category, package ) )

                # remove vcs directories
                for vcsdir in VCSDirs():
                    if vcsdir in subPackageList:
                        subPackageList.remove( vcsdir )
                if "__pycache__" in subPackageList:
                    subPackageList.remove( "__pycache__" )

                for subPackage in subPackageList:
                    if not os.path.isdir( os.path.join( directory, category, package, subPackage ) ) or subPackage in VCSDirs():
                        continue

                    dontBuildSubPackageList = self.getDontBuildPackagesList( os.path.join( directory, category, package ) )

                    if not subPackage in self.subpackages:
                        self.subpackages[ subPackage ] = []
                    if not subPackage in self.categories[ category ]:
                        _enabled = not category in dontBuildCategoryList and not package in dontBuildPackageList and not subPackage in dontBuildSubPackageList
                        self.categories[ category ].append( PackageObjectBase( category=category, subpackage=package, package=subPackage, enabled=_enabled ) )
                    self.subpackages[ subPackage ].append( category + "/" + package )

    def getCategory( self, package ):
        """ returns the category of this package """
        craftDebug.log.debug("getCategory: %s" % package)

        for cat in list(self.categories.keys()):
            if package in self.categories[ cat ]:
                craftDebug.log.debug("getCategory: found category %s for package %s" % (cat, package))
                return cat
        return False

    def isCategory( self, category ):
        """ returns whether a certain category exists """
        return category in list(self.categories.keys())

    def isPackage( self, category, package ):
        """ returns whether a certain package exists within a category """
        return package in self.categories[ category ]

    def isVirtualPackage( self, category, package ):
        """ check if that package is of VirtualPackageBase """
        if not self.isPackage( category, package ):
            return False
        mod = getPackageInstance(category,package)
        for baseClassObject in mod.__class__.__bases__:
            if baseClassObject.__name__ == 'VirtualPackageBase': return True
        return False

    def getDontBuildPackagesList( self, path ):
        """ get a list of packages from a dont_build file"""
        plist = []
        if os.path.exists( os.path.join( path, "dont_build.txt" ) ):
            with open( os.path.join( path, "dont_build.txt" ), "r" ) as f:
                for line in f:
                    if line.strip().startswith('#'): continue
                    if not line.strip() == "":
                        plist.append(line.strip())
        return plist

    def getAllPackages( self, category ):
        """returns all packages of a category except those that are listed in a file 'dont_build.txt' in the category directory
        in case the category doesn't exist, nothing is returned"""
        if self.isCategory( category ):
            plist = []
            for _p in self.categories[ category ]:
                if _p:
                    plist.append(_p.package)
            return plist
        else:
            return

    def getPackageInstance(self, category, package):
        """return instance of class Package from package file"""
        fileName =  getFilename( category, package )
        pack = None
        mod = None
        if fileName.endswith(".py") and os.path.isfile(fileName):
            if not fileName in self._packageDict:
                craftDebug.log.debug("module to import: %s" % fileName)
                if not os.path.isfile( fileName ):
                    try:
                        mod = builtins.__import__( fileName )
                    except ImportError as e:
                        craftDebug.log.warning('import failed for module %s: %s' % (fileName, str(e)))
                        mod =  None
                else:
                    modulename = os.path.basename( fileName )[:-3].replace('.', '_')
                    loader = importlib.machinery.SourceFileLoader(modulename, fileName)
                    try:
                        mod = loader.load_module()
                    except Exception as e:
                        raise PortageException("Failed to load file %s" % fileName, category, package, e)
                if not mod is None:
                    subpackage, package = getSubPackage( category, package )
                    self._CURRENT_MODULE  = ( fileName, category,subpackage, package, mod )
                    pack = mod.Package( )
                    self._packageDict[ fileName ] = pack
                else:
                    raise PortageException("Failed to find package", category, package)
            else:
                pack = self._packageDict[ fileName ]
            return pack

    def getDefaultTarget( self, category, package ):
        """ returns the default package of a specified package """
        craftDebug.log.debug("getDefaultTarget: importing file %s" % getFilename(category, package))
        if not ( category and package ):
            return dict()

        info = _getSubinfo( category, package )
        if not info is None:
            return info.defaultTarget
        else:
            return None

    def getAllTargets( self, category, package ):
        """ returns all targets of a specified package """
        craftDebug.log.debug("getAllTargets: importing file %s" % getFilename(category, package))
        if not ( category and package ):
            return dict()
        info = _getSubinfo( category, package )
        if not info is None:
            tagDict = info.svnTargets.copy()
            tagDict.update( info.targets )
            craftDebug.log.debug(tagDict)
            return tagDict
        else:
            return dict()

    def getAllVCSTargets( self, category, package ):
        """ returns all version control system targets of a specified package,
            excluding those which do contain tags """
        craftDebug.log.debug("getAllVCSTargets: importing file %s" % getFilename(category, package))
        info = _getSubinfo(  category, package )
        if not info is None:
            tagDict = info.svnTargets
            for key in tagDict:
                craftDebug.log.debug('%s: %s' % (key, tagDict[key]))
            return tagDict
        else:
            return dict()

    def getUpdatableVCSTargets( self, category, package ):
        """ check if the targets are tags or not """
        targetDict = PortageInstance.getAllVCSTargets( category, package )
        retList = []
        for key in targetDict:
            url = targetDict[ key ]
            if url:
                sourceType = utils.getVCSType( url )
                if sourceType == "svn":
                    # for svn, ignore tags
                    if not url.startswith( "tags/" ) and not "/tags/" in url:
                        retList.append( key )
                elif sourceType == "git":
                    _, branch, tag = utils.splitVCSUrl( url )
                    if tag == "" and not branch.endswith("-patched"):
                        retList.append( key )
                elif not sourceType == "":
                    # for all other vcs types, simply rebuild everything for now
                    retList.append( key )
        return retList

    def getNewestVersion( self, category, package ):
        """ returns the newest version of this category/package """
        if( category == None ):
            raise PortageException( "Empty category", category, package )
        if not self.isCategory( category ):
            raise PortageException( "Could not find category", category, package )
        if not self.isPackage( category, package ):
            raise PortageException( "Could not find package", category, package )

        installed = InstallDB.installdb.getInstalledPackages(category, package )
        newest = PortageInstance.getDefaultTarget( category, package )

        for pack in installed:
            version = pack.getVersion()
            if not version or not newest: continue
            if utils.parse_version(newest) < utils.parse_version(version):
                newest = version
        return newest

    def getInstallables( self ):
        """ get all the packages that are within the portage directory """
        instList = list()
        for category in list(self.categories.keys()):
            for package in self.categories[ category ]:
                instList.append(package)
        return instList

# when importing this, this static Object should get added
PortageInstance = Portage()
for _dir in rootDirectories():
    PortageInstance.addPortageDir( _dir )

def getSubPackage( category, package ):
    """ returns package and subpackage names """
    """ in case no subpackage could be found, None is returned """
    if package in PortageInstance.subpackages:
        for entry in PortageInstance.subpackages[ package ]:
            cat, pac = entry.split("/")
            if cat == category: return pac, package
    return None, package



def getPackageInstance(category, package):
    """return instance of class Package from package file"""
    return PortageInstance.getPackageInstance(category, package)

def getDependencies( category, package, runtimeOnly = False ):
    """returns the dependencies of this package as list of strings:
    category/package"""

    subpackage, package = getSubPackage( category, package )
    if subpackage:
        craftDebug.log.debug("solving package %s/%s/%s %s" % (category, subpackage, package,
                                                          getFilename(category, package)))
    else:
        craftDebug.log.debug("solving package %s/%s %s" % (category, package, getFilename(category, package)))

    deps = []
    info = _getSubinfo(category, package)
    if not info is None:
        depDict = info.dependencies
        depDict.update( info.runtimeDependencies )
        if not runtimeOnly:
            depDict.update( info.buildDependencies )

        for line in depDict:
            (category, package) = line.split( "/" )
            version = PortageInstance.getNewestVersion( category, package )
            deps.append( [ category, package, version, depDict[ line ] ] )
    return deps

def parseListFile( filename ):
    """parses a csv file used for building a list of specific packages"""
    categoryList = []
    packageList = []
    infoDict = {}
    listFileObject = open( filename, 'r' )
    for line in listFileObject:
        if line.strip().startswith('#'): continue
        try:
            cat, pac, tar, plvl = line.split( ',' )
        except:
            continue
        categoryList.append( cat )
        packageList.append( pac )
        infoDict[ cat + "/" + pac ] = (tar, plvl)
    return categoryList, packageList, infoDict


def solveDependencies( category, package, depList, depType = DependencyType.Both, maxDepth = -1, ignoredPackages = None ):
    depList.reverse()
    if ( category == "" ):
        category = PortageInstance.getCategory( package )
        craftDebug.log.debug("found package in category %s" % category)

    pac = DependencyPackage( category, package, parent = None )
    depList = pac.getDependencies( depList, depType=depType, maxDepth = maxDepth, single = set(), ignoredPackages = ignoredPackages )

    depList.reverse()
    return depList

def printTargets( category, package ):
    targetsDict = PortageInstance.getAllTargets( category, package )
    defaultTarget = PortageInstance.getDefaultTarget( category, package )
    if 'svnHEAD' in targetsDict and not targetsDict['svnHEAD']:
        del targetsDict['svnHEAD']
    targetsDictKeys = list(targetsDict.keys())
    targetsDictKeys.sort()
    for i in targetsDictKeys:
        if defaultTarget == i:
            craftDebug.log.info('*', end=' ')
        else:
            craftDebug.log.info(' ', end=' ')
        craftDebug.log.info(i)

def _getSubinfo( category, package  ):
    pack = getPackageInstance( category, package  )
    if pack:
        return pack.subinfo
    return None


def readChildren( category, package ):
    craftDebug.log.debug("solving package %s/%s %s" % (category, package, getFilename(category, package)))
    subinfo = _getSubinfo( category, package  )

    if subinfo is None:
        return OrderedDict(), OrderedDict()

    runtimeDependencies = subinfo.runtimeDependencies
    buildDependencies = subinfo.buildDependencies

    commonDependencies = subinfo.dependencies
    runtimeDependencies.update(commonDependencies)
    buildDependencies.update(commonDependencies)
    return runtimeDependencies, buildDependencies

def isPackageUpdateable( category, package ):
    craftDebug.log.debug("isPackageUpdateable: importing file %s" % getFilename(category, package))
    subinfo = _getSubinfo( category, package )
    if not subinfo is None:
        if len( subinfo.svnTargets ) == 1 and not subinfo.svnTargets[ list(subinfo.svnTargets.keys())[0] ]:
            return False
        return len( subinfo.svnTargets ) > 0
    else:
        return False

def alwaysTrue( *dummyArgs):
    """we sometimes need a function that always returns True"""
    return True

def getHostAndTarget( hostEnabled, targetEnabled ):
    """used for messages"""
    msg = ""
    if hostEnabled or targetEnabled:
        msg += "("
        if hostEnabled:
            msg += "H"
        if hostEnabled and targetEnabled:
            msg += "/"
        if targetEnabled:
            msg += "T"
        msg += ")"
    return msg

def printCategoriesPackagesAndVersions( lines, condition, hostEnabled=alwaysTrue, targetEnabled=alwaysTrue ):
    """prints a number of 'lines', each consisting of category, package and version field"""
    def printLine( cat, pack, ver, hnt="" ):
        catlen = 25
        packlen = 25
        craftDebug.log.info(cat + " " * ( catlen - len( cat ) ) + pack + " " * ( packlen - len( pack ) ) + ver + hnt)

    printLine( 'Category', 'Package', 'Version' )
    printLine( '--------', '-------', '-------' )
    for category, package, version in lines:
        if condition( category, package, version ):
            printLine( category, package, version )

def printInstallables():
    """get all the packages that can be installed"""
    data = list()
    for p in PortageInstance.getInstallables():
        data.append((p.category,p.package, p.version))
    printCategoriesPackagesAndVersions( data, alwaysTrue )

def printPackagesForFileSearch(filename):
    packages = InstallDB.installdb.getPackagesForFileSearch(filename)
    for pId, filename in packages:
        category, packageName, version = pId.getPackageInfo()
        craftDebug.log.info("%s/%s: %s" % (category, packageName, filename))

def getPackagesCategories(packageName, defaultCategory = None):
    craftDebug.trace("getPackagesCategories for package name %s" % packageName)
    if defaultCategory is None:
        defaultCategory = craftSettings.get("General","EMERGE_DEFAULTCATEGORY","kde")

    packageList, categoryList = [], []
    if len( packageName.split( "/" ) ) == 1:
        if PortageInstance.isCategory( packageName ):
            craftDebug.log.debug("isCategory=True")
            packageList = PortageInstance.getAllPackages( packageName )
            categoryList = [ packageName ] * len(packageList)
        else:
            craftDebug.log.debug("isCategory=False")
            if PortageInstance.isCategory( defaultCategory ) and PortageInstance.isPackage( defaultCategory, packageName ):
                # prefer the default category
                packageList = [ packageName ]
                categoryList = [ defaultCategory ]
            else:
                if PortageInstance.getCategory( packageName ):
                    packageList = [ packageName ]
                    categoryList = [ PortageInstance.getCategory( packageName ) ]
    elif len( packageName.split( "/" ) ) == 2:
        [ cat, pac ] = packageName.split( "/" )
        if PortageInstance.isCategory( cat ):
            categoryList = [ cat ]
        else:
            return packageList, categoryList
        if len( categoryList ) > 0 and PortageInstance.isPackage( categoryList[0], pac ):
            packageList = [ pac ]
        if len( categoryList ) and len( packageList ):
            craftDebug.log.debug("added package %s/%s" % (categoryList[0], pac))
    else:
        craftDebug.log.error("unknown packageName")

    return packageList, categoryList


