## @package portage
#  @brief contains portage tree related functions
#  @note this file should replace all other related portage related files
import utils

import builtins
import imp
import os
import re
import sys
import portage_versions
import emergePlatform
import copy
from collections import OrderedDict
from EmergePackageObject import PackageObjectBase
from emerge_config import *
#a import to portageSearch infront of def getPackagesCategories to prevent the circular import with installdb


internalCategory = 'internal'
ROOTDIR = os.getenv( "KDEROOT" )

modDict = OrderedDict()
packageDict = OrderedDict()

def __import__( module ): # pylint: disable=W0622
    utils.debug( "module to import: %s" % module, 2 )
    if not os.path.isfile( module ):
        try:
            return builtins.__import__( module )
        except ImportError as e:
            utils.warning( 'import failed for module %s: %s' % (module, str(e)) )
            return None
    else:
        sys.path.append( os.path.dirname( module ) )
        modulename = os.path.basename( module ).replace('.py', '')

        suff_index = None
        for suff in imp.get_suffixes():
            if suff[0] == ".py":
                suff_index = suff
                break

        if suff_index is None:
            utils.die("no .py suffix found")

        with open( module ) as fileHdl:
            try:
                return imp.load_module( modulename.replace('.', '_'),
                fileHdl, module, suff_index )
            except ImportError as e:
                utils.warning( 'import failed for file %s: %s' % (module, e) )
                return None

class DependencyPackage(object):
    """ This class wraps each package and constructs the dependency tree
        original code is from dependencies.py, integration will come later...
        """
    def __init__( self, category, name, version , autoExpand = True ):
        self.category = category
        self.name = name
        self.version = version
        self.runtimeChildren = []
        self.buildChildren = []
        if autoExpand:
            self.__readChildren()

    def __hash__(self):
        return str( self.category + "/" +  self.name).__hash__()
        
    def __eq__( self, other ):
        return self.category == other.category and self.name == other.name and self.version == other.version

    def __ne__( self, other ):
        return self.category != other.category or self.name != other.name or self.version != other.version

    def ident( self ):
        return [ self.category, self.name, self.version, PortageInstance.getDefaultTarget( self.category, self.name, self.version ) ]

    def __readChildren( self ):
        runtimeDependencies, buildDependencies = readChildren( self.category, self.name, self.version )
        self.runtimeChildren = self.__readDependenciesForChildren( list(runtimeDependencies.keys()) )
        self.buildChildren = self.__readDependenciesForChildren( list(buildDependencies.keys()) )

    def __readDependenciesForChildren( self, deps ):
        children = []
        if deps:
            for line in deps:
                ( category, package ) = line.split( "/" )
                utils.debug( "category: %s, name: %s" % ( category, package ), 1 )
                version = PortageInstance.getNewestVersion( category, package )
                if not line in list(packageDict.keys()):
                    p = DependencyPackage( category, package, version, False )
                    utils.debug( "adding package p %s/%s-%s" % ( category, package, version ), 1 )
                    packageDict[ line ] = p
                    p.__readChildren()
                else:
                    p = packageDict[ line ]
                children.append( p )
        return children

    def getDependencies( self, depList=None, dep_type="both", single = set() ):
        """ returns all dependencies """
        if depList is None:
            depList = []
        if dep_type == "runtime":
            children = self.runtimeChildren
        elif dep_type == "buildtime":
            children = self.buildChildren
        else:
            children = self.runtimeChildren + self.buildChildren
            
        single.add(self)
        for p in children:
            if not p in single and not p in depList\
            and not ("%s/%s" % (p.category, p.name)) in PortageInstance.ignores:
                p.getDependencies( depList, dep_type,single )
                    
        #if self.category != internalCategory:
        if not self in depList and not ("%s/%s" % (self.category, self.name)) in PortageInstance.ignores:
            depList.append( self )



        return depList

def buildType():
    """return currently selected build type"""
    return os.getenv( "EMERGE_BUILDTYPE" )

def rootDirectories():
    # this function should return all currently set portage directories
    if os.getenv( "EMERGE_PORTAGE_ROOT" ):
        rootDirs = os.getenv( "EMERGE_PORTAGE_ROOT" ).split( ";" )
    else:
        rootDirs = []
    if len( rootDirs ) == 0:
        rootDirs = [ os.path.join( os.getenv( "KDEROOT" ), "emerge", "portage" ) ]
    return rootDirs

def rootDir():
    # this function should return the portage directory, either the first set
    # via the environment, or the default one
    # keep this function for compat reasons
    return rootDirectories()[0]

def rootDirForCategory( category ):
    # this function should return the portage directory where it finds the
    # first occurance of a category or the default value
    for i in rootDirectories():
        if category and os.path.exists( os.path.join( i, category ) ):
            return i
    # as a fall back return the default even if it might be wrong
    return os.path.join( os.getenv( "KDEROOT" ), "emerge", "portage" )

def rootDirForPackage( category, package ):
    # this function should return the portage directory where it finds the
    # first occurance of a package or the default value
    package, subpackage = getSubPackage( category, package )
    if category and package:
        if subpackage:
            for i in rootDirectories():
                if os.path.exists( os.path.join( i, category, package, subpackage ) ):
                    return i
        else:
            for i in rootDirectories():
                if os.path.exists( os.path.join( i, category, package ) ):
                    return i
    # as a fall back return the default even if it might be wrong
    return os.path.join( os.getenv( "KDEROOT" ), "emerge", "portage" )

def getDirname( category, package ):
    """ return absolute pathname for a given category and package """
    _package, _subpackage = getSubPackage( category, package )
    if category and _package:
        if _subpackage:
            return os.path.join( rootDirForPackage( category, package ), category, _package, _subpackage )
        else:
            return os.path.join( rootDirForPackage( category, package ), category, package )
    else:
        return ""

def getFilename( category, package, version ):
    """ return absolute filename for a given category, package and version """
    return os.path.join( getDirname( category, package ), "%s-%s.py" % ( package, version ) )

def getCategoryPackageVersion( path ):
    utils.debug( "getCategoryPackageVersion: %s" % path, 2 )
    head, fullFileName = os.path.split( path )
    for rd in rootDirectories():
        if head.startswith(rd):
            head = head.replace(rd + os.sep, "")
            break

    if len( head.split( os.sep ) )  == 3:
        category, _dummy, package = head.split( os.sep )
    else:
        head, package = os.path.split( head )
        head, category = os.path.split( head )

    filename = os.path.splitext( fullFileName )[0]
    package, version = utils.packageSplit( filename )
    utils.debug( "category: %s, package: %s, version: %s" % ( category, package, version ), 1 )
    return [ category, package, version ] # TODO: why a list and not a tuple?

def VCSDirs():
    return [ '.svn', 'CVS', '.hg', '.git' ]

class Portage(object):
    def __init__( self ):
        """ """
        self.categories = {}
        self.subpackages = {}
        self.portages = {}
        self.ignores = set()
        if emergeSettings.contains("Portage","PACKAGE_IGNORES"):
            for p in emergeSettings.get("Portage","PACKAGE_IGNORES").split(";"):
                self.ignores.add(p)
            

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

                    if not subPackage in list(self.subpackages.keys()):
                        self.subpackages[ subPackage ] = []
                    if not subPackage in self.categories[ category ]:
                        _enabled = not category in dontBuildCategoryList and not package in dontBuildPackageList and not subPackage in dontBuildSubPackageList
                        self.categories[ category ].append( PackageObjectBase( category=category, subpackage=package, package=subPackage, enabled=_enabled ) )
                    self.subpackages[ subPackage ].append( category + "/" + package )


    def getCategory( self, package ):
        """ returns the category of this package """
        utils.debug( "getCategory: %s" % package, 2 )

        for cat in list(self.categories.keys()):
            if package in self.categories[ cat ]:
                utils.debug( "found: category %s for package %s" % ( cat, package ), 1 )
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
        version = self.getNewestVersion( category, package )
        mod = __import__( getFilename( category, package, version ) )
        if hasattr( mod, 'Package' ):
            for baseClassObject in mod.Package.__bases__:
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

    def getPackageInstance(self, category, package, buildtarget=None):
        """return instance of class Package from package file"""
        version = self.getNewestVersion( category, package )
        fileName = getFilename( category, package, version )
        module = __import__( fileName )
        p = module.Package()
        if buildtarget == None:
            buildtarget = findPossibleTargets( category, package, version )
        p.setup(fileName, category, package, version, buildtarget)
        return p

    def getDefaultTarget( self, category, package, version ):
        """ returns the default package of a specified package """
        utils.debug( "getDefaultTarget: importing file %s" % getFilename( category, package, version ), 1 )
        if not ( category and package and version ):
            return dict()
        mod = __import__( getFilename( category, package, version ) )
        if hasattr( mod, 'subinfo' ):
            return mod.subinfo().defaultTarget
        else:
            return None

    def getMetaData( self, category, package, version ):
        """ returns all targets of a specified package """
        utils.debug( "getMetaData: importing file %s" % getFilename( category, package, version ), 1 )
        if not ( category and package and version ):
            return dict()
        mod = __import__( getFilename( category, package, version ) )
        if hasattr( mod, 'subinfo' ):
            info = mod.subinfo()
            tmpdict = dict()
            if not info.categoryName == "":
                tmpdict['categoryName'] = info.categoryName
            if not info.shortDescription == "":
                tmpdict['shortDescription'] = info.shortDescription
            if not info.description == "":
                tmpdict['description'] = info.description
            if not info.homepage == "":
                tmpdict['homepage'] = info.homepage
            tmpdict['withCompiler'] = info.options.package.withCompiler
            utils.debug( tmpdict, 2 )
            return tmpdict
        else:
            return {'withCompiler': True}

    def getAllTargets( self, category, package, version ):
        """ returns all targets of a specified package """
        utils.debug( "getAllTargets: importing file %s" % getFilename( category, package, version ), 1 )
        if not ( category and package and version ):
            return dict()
        mod = __import__( getFilename( category, package, version ) )
        if hasattr( mod, 'subinfo' ):
            info = mod.subinfo()
            tagDict = info.svnTargets
            tagDict.update( info.targets )
            utils.debug( tagDict, 2 )
            return tagDict
        else:
            return dict()

    def getAllVCSTargets( self, category, package, version ):
        """ returns all version control system targets of a specified package,
            excluding those which do contain tags """
        utils.debug( "getAllVCSTargets: importing file %s" % getFilename( category, package, version ), 1 )
        mod = __import__( getFilename( category, package, version ) )
        if hasattr( mod, 'subinfo' ):
            info = mod.subinfo()
            tagDict = info.svnTargets
            for key in tagDict:
                utils.debug( '%s: %s' % ( key, tagDict[key] ), 2 )
            return tagDict
        else:
            return dict()

    def getUpdatableVCSTargets( self, category, package, version ):
        """ check if the targets are tags or not """
        targetDict = PortageInstance.getAllVCSTargets( category, package, version )
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
            utils.die( "Empty category for package '%s'" % package )
        if not self.isCategory( category ):
            utils.die( "could not find category '%s'" % category )
        if not self.isPackage( category, package ):
            utils.die( "could not find package '%s' in category '%s'" % ( package, category ) )

        versions = []
        for fileName in os.listdir( getDirname( category, package ) ):
            (shortname, ext) = os.path.splitext( fileName )
            if ( ext != ".py" ):
                continue
            if ( shortname.startswith( package ) ):
                versions.append( shortname )

        tmpver = ""
        for ver in versions:
            if ( tmpver == "" ):
                tmpver = ver
            else:
                ret = portage_versions.pkgcmp(portage_versions.pkgsplit(ver), \
                                              portage_versions.pkgsplit(tmpver))
                if ( ret == 1 ):
                    tmpver = ver

        ret = utils.packageSplit( tmpver )
        #print "ret:", ret
        return ret[ 1 ]

    def getInstallables( self ):
        """ get all the packages that are within the portage directory """
        instList = list()
        for category in list(self.categories.keys()):
            for package in self.categories[ category ]:
                for script in os.listdir( getDirname( category, package.package ) ):
                    if script.endswith( '.py' ):
                        version = script.replace('.py', '').replace(package.package + '-', '')
                        instList.append([category, package.package, version])
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
    return package, None

def findPossibleTargets( category, package, version, buildtype=''): # pylint: disable=W0613
    """ this function tries to guess which target got used by looking at the different image directories """
    target = PortageInstance.getDefaultTarget( category, package, version )
    buildroot = os.path.join( ROOTDIR, "build", category, "%s-%s" % ( package, version ) )

    if not os.path.exists( buildroot ):
        return target

    for directory in os.listdir( buildroot ):
        if os.path.isdir( os.path.join( buildroot, directory ) ):
            if directory.startswith( "image" ) and directory != "image":
                particles = directory.split( '-' )[ 1: ] # the first part should be image- anyway
                if len(particles) == 1 and \
                   not particles[0] in [os.getenv( "KDECOMPILER" ), \
                                        os.getenv( "EMERGE_BUILDTYPE" ), \
                                        os.getenv( "EMERGE_TARGET_PLATFORM" ), \
                                        "WIN32"]:
                    return particles[0]
                elif len(particles) == 3:
                    _platform, _buildType, _target = particles
                elif len(particles) == 4 and emergePlatform.isCrossCompilingEnabled():
                    _platform, _buildType, _buildArch, _target = particles
                elif len(particles) >= 4 and not emergePlatform.isCrossCompilingEnabled():
                    _platform, _buildType = particles[0:2]
                    _target = '-'.join(particles[2:])
                else:
                    return target
                if _platform == os.getenv( "KDECOMPILER" ) and \
                   _buildType == os.getenv( "EMERGE_BUILDTYPE" ):
                    return _target
    return target

def getPackageInstance(category, package, buildtarget=None):
    """return instance of class Package from package file"""
    return PortageInstance.getPackageInstance(category, package, buildtarget)

def getDependencies( category, package, version, runtimeOnly=False ):
    """returns the dependencies of this package as list of strings:
    category/package"""
    if not os.path.isfile( getFilename( category, package, version ) ):
        utils.die( "package name %s/%s-%s unknown" % ( category, package, version ) )

    package, subpackage = getSubPackage( category, package )
    if subpackage:
        utils.debug( "solving package %s/%s/%s-%s %s" % ( category, subpackage, package, version, getFilename( category, package, version ) ), 0 )
    else:
        utils.debug( "solving package %s/%s-%s %s" % ( category, package, version, getFilename( category, package, version ) ), 0 )
        subpackage = package
    
    deps = []
    for pkg in [ subpackage ]:
        mod = __import__( getFilename( category, subpackage, version ) )
        if hasattr( mod, 'subinfo' ):
            info = mod.subinfo()
            depDict = info.hardDependencies
            depDict.update( info.dependencies )
            depDict.update( info.runtimeDependencies )
            if not runtimeOnly:
                depDict.update( info.buildDependencies )

            for line in list(depDict.keys()):
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


def solveDependencies( category, package, version, depList, dep_type='both' ):
    depList.reverse()
    if ( category == "" ):
        category = PortageInstance.getCategory( package )
        utils.debug( "found package in category %s" % category, 2 )
    if ( version == "" ):
        version = PortageInstance.getNewestVersion( category, package )
        utils.debug( "found package with newest version %s" % version, 2 )

    pac = DependencyPackage( category, package, version )
    depList = pac.getDependencies( depList, dep_type=dep_type )

    depList.reverse()
    return depList

def printTargets( category, package, version ):
    targetsDict = PortageInstance.getAllTargets( category, package, version )
    defaultTarget = PortageInstance.getDefaultTarget( category, package, version )
    if 'svnHEAD' in targetsDict and not targetsDict['svnHEAD']:
        del targetsDict['svnHEAD']
    targetsDictKeys = list(targetsDict.keys())
    targetsDictKeys.sort()
    for i in targetsDictKeys:
        if defaultTarget == i:
            print('*', end=' ')
        else:
            print(' ', end=' ')
        print(i)

def readChildren( category, package, version ):
    identFileName = getFilename( category, package, version )
    if not os.path.isfile( identFileName ):
        utils.die( "package name %s/%s-%s unknown" % ( category, package, version ) )

    # if we are an emerge internal package and already in the dictionary, ignore childrens
    # To avoid possible endless recursion this may be also make sense for all packages
    if category == internalCategory and identFileName in list(modDict.keys()):
        return OrderedDict(), OrderedDict()
    package, subpackage = getSubPackage( category, package )
    if subpackage:
        utils.debug( "solving package %s/%s/%s-%s %s" % ( category, subpackage, package, version, getFilename( category, package, version ) ), 2 )
    else:
        utils.debug( "solving package %s/%s-%s %s" % ( category, package, version, getFilename( category, package, version ) ), 2 )
    if not identFileName in list(modDict.keys()):
        mod = __import__( identFileName )
        modDict[ identFileName ] = mod
    else:
        mod = modDict[ identFileName ]

    if utils.envAsBool('EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES') and hasattr( mod, 'Package' ):
        _package = mod.Package()
        subinfo = _package.subinfo
    elif hasattr( mod, 'subinfo' ):
        subinfo = mod.subinfo()
    else:
        return OrderedDict(), OrderedDict()

    runtimeDependencies = subinfo.runtimeDependencies or OrderedDict()
    buildDependencies = subinfo.buildDependencies or OrderedDict()

    # hardDependencies
    commonDependencies = subinfo.hardDependencies
    commonDependencies.update( subinfo.dependencies )
    runtimeDependencies.update(commonDependencies)
    buildDependencies.update(commonDependencies)

    return runtimeDependencies, buildDependencies

def isHostBuildEnabled( category, package, version ):
    """ returns whether this package's host build is enabled. This will only work if
        isCrossCompilingEnabled() == True """

    if emergePlatform.isCrossCompilingEnabled():
        mod = __import__( getFilename( category, package, version ) )
        if hasattr( mod, 'subinfo' ):
            info = mod.subinfo()
            return not info.disableHostBuild
        else:
            return False
    else:
        utils.die( "This function must not be used outside of cross-compiling environments!" )

def isTargetBuildEnabled( category, package, version ):
    """ returns whether this package's target build is enabled. This will only work if
        isCrossCompilingEnabled() == True """

    if emergePlatform.isCrossCompilingEnabled():
        mod = __import__( getFilename( category, package, version ) )
        if hasattr( mod, 'subinfo' ):
            info = mod.subinfo()
            return not info.disableTargetBuild
        else:
            return False
    else:
        utils.die( "This function must not be used outside of cross-compiling environments!" )

def isPackageUpdateable( category, package, version ):
    utils.debug( "isPackageUpdateable: importing file %s" % getFilename( category, package, version ), 2 )
    mod = __import__( getFilename( category, package, version ) )
    if hasattr( mod, 'subinfo' ):
        info = mod.subinfo()
        if len( info.svnTargets ) == 1 and not info.svnTargets[ list(info.svnTargets.keys())[0] ]:
            return False
        return len( info.svnTargets ) > 0
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
        print(cat + " " * ( catlen - len( cat ) ) + pack + " " * ( packlen - len( pack ) ) + ver, hnt)

    printLine( 'Category', 'Package', 'Version' )
    printLine( '--------', '-------', '-------' )
    for category, package, version in lines:
        if emergePlatform.isCrossCompilingEnabled():
            msg = getHostAndTarget( hostEnabled( category, package, version ), targetEnabled( category, package, version ) )
        else:
            msg = ""
        if condition( category, package, version ):
            printLine( category, package, version, msg )

def printInstallables():
    """get all the packages that can be installed"""
    printCategoriesPackagesAndVersions( PortageInstance.getInstallables(), alwaysTrue )
    

def printInstalled():
    """get all the packages that are already installed"""
    printCategoriesPackagesAndVersions( PortageInstance.getInstallables(), isInstalled )    

def isInstalled( category, package, version, buildtype='' ):
    """ deprecated, use InstallDB.installdb.isInstalled() instead """
    utils.debug( "isInstalled(%s, %s, %s, %s)" % (category, package, version, buildtype), 2 )
    # find in old style database
    path = utils.etcDir()
    fileName = os.path.join(path,'installed')
    found = False
    if os.path.isfile( fileName ):
        with open( fileName, "rt" ) as f:
            for line in f.read().splitlines():
                if not line: continue # Ignore empty lines
                (_category, _packageVersion) = line.split( "/" )
                (_package, _version) = utils.packageSplit(_packageVersion)
                if category != '' and version != '' and category == _category and package == _package and version == _version:
                    found = True
                    break
                elif category == '' and version == '' and package == _package:
                    found = True
                    break
        utils.debug("...%s found in main database" % (' ' if found else ' not'), 2 )
        if found:
            return True

    # find in release mode database
    if buildtype != '':
        fileName = os.path.join(path,'installed-' + buildtype )
        if os.path.isfile( fileName ):
            with open( fileName, "rt" ) as f:
                for line in f.read().splitlines():
                    if not line or line == "":
                        continue
                    (_category, _packageVersion) = line.split( "/" )
                    (_package, _version) = utils.packageSplit(_packageVersion)
                    if category != '' and version != '' and category == _category and package == _package and version == _version:
                        found = True
                        break
                    elif category == '' and version == '' and package == _package:
                        found = True
                        break
            utils.debug( "...%s found in %s database" % ( (' ' if found else ' not'), buildtype), 2 )
            if found:
                return True

    # try to detect packages from the installer
    binary = utils.checkManifestFile( os.path.join( os.getenv( "KDEROOT" ), "manifest",
            package + "-" + version + "-bin.ver"), category, package, version )
    lib = utils.checkManifestFile( os.path.join( os.getenv( "KDEROOT" ), "manifest",
            package + "-" + version + "-lib.ver"), category, package, version )
    found = found or binary or lib

    if not utils.envAsBool("EMERGE_VERSIONING", default=True):
        # check for any installation except data packages
        if not os.path.exists(os.path.join( os.getenv( "KDEROOT" ), "manifest" ) ):
            return False
        if package.endswith( "-src" ):
            package = package[:-4]
        for filename in os.listdir( os.path.join( os.getenv( "KDEROOT" ), "manifest" ) ):
            if filename.startswith( package ) and not \
                    filename.startswith( package + "-data" ):
                return True
    return False

def findInstalled( category, package):
    """ deprecated, use InstallDB.installdb.findInstalled() instead """
    fileName = os.path.join(utils.etcDir(), "installed" )
    if ( not os.path.isfile( fileName ) ):
        return None

    ret = None
    regexStr = "^%s/%s-(.*)$" % ( category, re.escape(package) )
    regex = re.compile( regexStr )
    with open( fileName, "rt" ) as f:
        for line in f.read().splitlines():
            match = regex.match( line )
            if match:
                utils.debug( "found: " + match.group(1), 2 )
                ret = match.group(1)
    return ret

def addInstalled( category, package, version, buildtype='' ):
    """ deprecated, use InstallDB.installdb.addInstalled() instead """
    utils.debug( "addInstalled called", 2 )
    # write a line to etc/portage/installed,
    # that contains category/package-version
    path = os.path.join(utils.etcDir() )
    if ( not os.path.isdir( path ) ):
        os.makedirs( path )
    if buildtype != '':
        fileName = 'installed-' + buildtype
    else:
        fileName = 'installed'
    utils.debug("installing package %s - %s into %s" % (package, version, fileName), 2)
    if( os.path.isfile( os.path.join( path, fileName ) ) ):
        with open( os.path.join( path, fileName ), "rt" ) as f:
            for line in f:
                if line.startswith( "%s/%s-%s" % ( category, package, version) ):
                    utils.warning( "version already installed" )
                    return
                elif line.startswith( "%s/%s-" % ( category, package ) ):
                    utils.die( "Already installed, this should not happen" )
    with open( os.path.join( path, fileName ), "at" ) as f:
        f.write( "%s/%s-%s\r\n" % ( category, package, version ) )

def remInstalled( category, package, version, buildtype='' ):
    """ deprecated, use InstallDB.installdb.remInstalled() instead """
    utils.debug( "remInstalled called", 2 )
    if buildtype != '':
        fileName = 'installed-' + buildtype
    else:
        fileName = 'installed'
    utils.debug("removing package %s - %s from %s" % (package, version, fileName), 2)
    dbFileName = os.path.join(utils.etcDir(), fileName )
    tmpdbfile = os.path.join(utils.etcDir(), "TMPinstalled" )
    found = False
    if os.path.exists( dbFileName ):
        with open( dbFileName, "rt" ) as dbFile:
            with open( tmpdbfile, "wt" ) as tfile:
                for line in dbFile:
                    ## \todo the category should not be part of the search string
                    ## because otherwise it is not possible to unmerge package using
                    ## the same name but living in different categories
                    if not line.startswith("%s/%s" % ( category, package ) ):
                        tfile.write( line )
                    else:
                        found = True
        os.remove( dbFileName )
        os.rename( tmpdbfile, dbFileName )
    return found

import portageSearch

def getPackagesCategories(packageName, defaultCategory = None):
    utils.debug( "getPackagesCategories for package name %s" % packageName, 1 )
    if defaultCategory is None:
        if "EMERGE_DEFAULTCATEGORY" in os.environ:
            defaultCategory = os.environ["EMERGE_DEFAULTCATEGORY"]
        else:
            defaultCategory = "kde"

    packageList, categoryList = [], []
    if len( packageName.split( "/" ) ) == 1:
        if PortageInstance.isCategory( packageName ):
            utils.debug( "isCategory=True", 2 )
            packageList = PortageInstance.getAllPackages( packageName )
            categoryList = [ packageName ] * len(packageList)
        else:
            utils.debug( "isCategory=False", 2 )
            if PortageInstance.isCategory( defaultCategory ) and PortageInstance.isPackage( defaultCategory, packageName ):
                # prefer the default category
                packageList = [ packageName ]
                categoryList = [ defaultCategory ]
            else:
                if PortageInstance.getCategory( packageName ):
                    packageList = [ packageName ]
                    categoryList = [ PortageInstance.getCategory( packageName ) ]
                else:
                    portageSearch.printSearch("",packageName)
    elif len( packageName.split( "/" ) ) == 2:
        [ cat, pac ] = packageName.split( "/" )
        if PortageInstance.isCategory( cat ):
            categoryList = [ cat ]
        else:
            portageSearch.printSearch(cat,pac)
            return packageList, categoryList
        if len( categoryList ) > 0 and PortageInstance.isPackage( categoryList[0], pac ):
            packageList = [ pac ]
        if len( categoryList ) and len( packageList ):
            utils.debug( "added package %s/%s" % ( categoryList[0], pac ), 2 )
        else:
            portageSearch.printSearch(cat,pac)
    else:
        utils.error( "unknown packageName" )

    return packageList, categoryList


