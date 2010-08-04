## @package portage 
#  @brief contains portage tree related functions
#  @note this file should replace all other related portage related files
import utils

import __builtin__
import imp
import os
import re
import sys
import portage_versions
import platform

def __import__( module ):
    utils.debug( "module to import: %s" % module, 2 )
    if not os.path.isfile( module ):
        return __builtin__.__import__( module )
    else:
        sys.path.append( os.path.dirname( module ) )
        fileHdl = open( module )
        modulename = os.path.basename( module ).replace('.py', '')

        suff_index = None
        for suff in imp.get_suffixes():
            if suff[0] == ".py":
                suff_index = suff
                break

        if suff_index is None:
            utils.die("no .py suffix found")

        return imp.load_module( modulename.replace('.', '_'), 
            fileHdl, module, suff_index )

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
        if os.path.exists( os.path.join( i, category ) ):
            return i
    # as a fall back return the default even if it might be wrong
    return os.path.join( os.getenv( "KDEROOT" ), "emerge", "portage" )

def rootDirForPackage( category, package ):
    # this function should return the portage directory where it finds the
    # first occurance of a package or the default value
    for i in rootDirectories():
        if os.path.exists( os.path.join( i, category, package ) ):
            return i
    # as a fall back return the default even if it might be wrong
    return os.path.join( os.getenv( "KDEROOT" ), "emerge", "portage" )

def etcDir():
    return os.path.join( os.getenv( "KDEROOT" ), "etc", "portage" )

def getDirname( category, package ):
    """ return absolute pathname for a given category and package """
    file = os.path.join( rootDirForPackage( category, package ), category, package )
    return file
    
def getFilename( category, package, version ):
    """ return absolute filename for a given category, package and version """
    file = os.path.join( getDirname( category, package ), "%s-%s.py" % ( package, version ) )
    return file

def getCategoryPackageVersion( path ):
    utils.debug( "getCategoryPackageVersion: %s" % path ,2 )
    ( head, file ) = os.path.split( path )
    ( head, package ) = os.path.split( head )
    ( head, category ) = os.path.split( head )

    (filename, ext) = os.path.splitext( file )
    ( package, version ) = packageSplit( filename )
    utils.debug( "category: %s, package: %s, version: %s" % ( category, package, version ), 1 )
    return [ category, package, version ]

class Portage:
    def __init__( self ):
        """ """
        self.categories = {}
        self.portages = {}

    def addPortageDir( self, dir ):
        """ adds the categories and packages of a portage directory """
        if not os.path.exists( dir ): return

        categoryList = os.listdir( dir )

        # remove vcs directories
        for vcsdir in [ '.svn', 'CVS', '.hg', '.git' ]:
            if vcsdir in categoryList:
                categoryList.remove( vcsdir )

        self.portages[ dir ] = []
        for category in categoryList:
            if not os.path.isdir( os.path.join( dir, category ) ): continue
            if category in self.categories.keys(): continue

            self.portages[ dir ].append( category )

            packageList = os.listdir( os.path.join( dir, category ) )

            # remove vcs directories
            for vcsdir in [ '.svn', 'CVS', '.hg', '.git' ]:
                if vcsdir in packageList:
                    packageList.remove( vcsdir )

            self.categories[ category ] = []
            for package in packageList:
                if not os.path.isdir( os.path.join( dir, category, package ) ): continue
                if not package in self.categories[ category ]:
                    self.categories[ category ].append( package )
            

    def getCategory( self, package ):
        """ returns the category of this package """
        utils.debug( "getCategory: %s" % package, 2 )

        for cat in self.categories.keys():
            if package in self.categories[ cat ]:
                utils.debug( "found: category %s for package %s" % ( cat, package ), 1 )
                return cat
        return False

    def isCategory( self, category ):
        """ returns whether a certain category exists """
        return category in self.categories.keys()

    def isPackage( self, category, package ):
        """ returns whether a certain package exists within a category """
        return package in self.categories[ category ]

    def getAllPackages( self, category ):
        """ returns all packages of a category except those that are listed in a file 'dont_build.txt' in the category directory """
        """ in case the category doesn't exist, nothing is returned """
        if self.isCategory( category ):
            plist = self.categories[ category ]
            if os.path.exists( os.path.join( rootDirForCategory( category ), category, "dont_build.txt" ) ):
                f = open( os.path.join( rootDirForCategory( category ), category, "dont_build.txt" ), "r" )
                for line in f:
                    try:
                        plist.remove( line.strip() )
                    except:
                        utils.warning( "couldn't remove package %s from category %s's package list" % ( line.strip(), category ) )
            return plist
        else:
            return

    def getPackageInstance(self, category, package, buildtarget=None):
        """return instance of class Package from package file"""
        if platform.isCrossCompilingEnabled() \
        or os.getenv("EMERGE_SOURCEONLY") == "True" or os.getenv("EMERGE_SOURCEONLY") == "1":
            sp = self.getCorrespondingSourcePackage( package )
            if sp:
                category = sp[0]
                package = sp[1]
                
        version = self.getNewestVersion( category, package )
        fileName = getFilename( category, package, version )
        module = __import__( fileName )
        p = module.Package()
        p.setup(fileName, category, package, version, buildtarget)
        return p
    
    def getDefaultTarget( self, category, package, version ):
        """ returns the default package of a specified package """
        utils.debug( "importing file %s" % getFilename( category, package, version ), 1 )
        mod = __import__( getFilename( category, package, version ) )
        if hasattr( mod, 'subinfo' ):
            info = mod.subinfo()
            return mod.subinfo().defaultTarget
        else:
            return None

    def getAllTargets( self, category, package, version ):
        """ returns all targets of a specified package """
        utils.debug( "importing file %s" % getFilename( category, package, version ), 1 )
        mod = __import__( getFilename( category, package, version ) )
        if hasattr( mod, 'subinfo' ):
            info = mod.subinfo()
            tagDict = info.svnTargets
            tagDict.update( info.targets )
            utils.debug( tagDict )
            return tagDict
        else:
            return dict()

    def getNewestVersion( self, category, package ):
        """ returns the newest version of this category/package """
        if( category == None ):
            utils.die( "Empty category for package '%s'" % package )
        if not self.isCategory( category ):
            utils.die( "could not find category '%s'" % category )
        if not self.isPackage( category, package ):
            utils.die( "could not find package '%s' in category '%s'" % ( package, category ) )

        versions = []
        for file in os.listdir( getDirname( category, package ) ):
            (shortname, ext) = os.path.splitext( file )
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

        ret = packageSplit( tmpver )
        #print "ret:", ret
        return ret[ 1 ]

    def getInstallables( self ):
        """ get all the packages that are within the portage directory """
        instList = list()
        for category in self.categories.keys():
            for package in self.categories[ category ]:
                for script in os.listdir( getDirname( category, package ) ):
                    if script.endswith( '.py' ):
                        version = script.replace('.py', '').replace(package + '-', '')
                        instList.append([category, package, version])
        return instList
        
    def getCorrespondingSourcePackage( self, package ):
        category = self.getCategory( package + "-src" )
        if category:
            # we found a corresponding package
            utils.debug( "replacing package %s with its source package" % ( package ), 1 )
            return [ category, package + "-src" ]
        else:
            return False


# when importing this, this static Object should get added
PortageInstance = Portage()
for _dir in rootDirectories():
    PortageInstance.addPortageDir( _dir )

def getPackageInstance(category, package, buildtarget=None):
    """return instance of class Package from package file"""
    return PortageInstance.getPackageInstance(category, package, buildtarget)

def isVersion( part ):
    ver_regexp = re.compile("^(cvs\\.)?(\\d+)((\\.\\d+)*)([a-z]?)((_(pre|p|beta|alpha|rc)\\d*)*)(-r(\\d+))?$")
    if ver_regexp.match( part ):
        return True
    else:
        return False

def packageSplit( fullname ):
    """ instead of using portage_versions.catpkgsplit use this function now """
    splitname = fullname.split('-')
    for x in range( len( splitname ) ):
        if isVersion( splitname[ x ] ):
            break
    package = splitname[ 0 ]
    version = splitname[ x ]
    for part in splitname[ 1 : x ]:
        package += '-' + part
    for part in splitname[ x  + 1: ]:
        version += '-' + part
    return [ package, version ]

def getDependencies( category, package, version ):
    """
    returns the dependencies of this package as list of strings:
    category/package
    """
    if not os.path.isfile( getFilename( category, package, version ) ):
        utils.die( "package name %s/%s-%s unknown" % ( category, package, version ) )

    utils.debug( "solving package %s/%s-%s %s" % ( category, package, version, getFilename( category, package, version ) ), 2 )
    mod = __import__( getFilename( category, package, version ) )

    deps = []
    if hasattr( mod, 'subinfo' ):
        info = mod.subinfo()
        for line in info.hardDependencies.keys():
            (category, package) = line.split( "/" )
            version = PortageInstance.getNewestVersion( category, package )
            deps.append( [ category, package, version, info.hardDependencies[ line ] ] )

    return deps

def solveDependencies( category, package, version, deplist ):
    if platform.isCrossCompilingEnabled() \
    or os.getenv("EMERGE_SOURCEONLY") == "True" or os.getenv("EMERGE_SOURCEONLY") == "1":
        sp = PortageInstance.getCorrespondingSourcePackage( package )
        if sp:
            # we found such a package and we're allowed to replace it
            category = sp[0]
            package = sp[1]
            version = PortageInstance.getNewestVersion( category, package )

    if ( category == "" ):
        category = PortageInstance.getCategory( package )

    if ( version == "" ):
        version = PortageInstance.getNewestVersion( category, package )

    tag = 1
    if ( tag == "" ):
        tag = PortageInstance.getAllTargets( category, package, version ).keys()[ 0 ]

    if [ category, package, version, tag ] in deplist:
        deplist.remove( [ category, package, version, tag ] )

    deplist.append( [ category, package, version, tag ] )

    mydeps = getDependencies( category, package, version )
#    if verbose() >= 1:
#        print "mydeps:", mydeps
    for dep in mydeps:
        solveDependencies( dep[0], dep[1], dep[2], deplist )
    # if package not in list, prepend it to list
    # get deps of this package
    # for every dep call solvedeps
    #return deplist

def printTargets( category, package, version ):
    """ """
    targetsDict = PortageInstance.getAllTargets( category, package, version )
    defaultTarget = PortageInstance.getDefaultTarget( category, package, version )
    if not targetsDict['svnHEAD']:
        del targetsDict['svnHEAD']
    targetsDictKeys = targetsDict.keys()
    targetsDictKeys.sort()
    for i in targetsDictKeys:
        if defaultTarget == i:
            print '*',
        else:
            print ' ',
        print i

def isPackageUpdateable( category, package, version ):
    utils.debug( "importing file %s" % getFilename( category, package, version ), 2 )
    mod = __import__( getFilename( category, package, version ) )
    if hasattr( mod, 'subinfo' ):
        info = mod.subinfo()
        if len( info.svnTargets ) is 1 and not info.svnTargets[ info.svnTargets.keys()[0] ]:
            return False
        return len( info.svnTargets ) > 0
    else:
        return False

def printCategoriesPackagesAndVersions(lines, condition):
    """prints a number of 'lines', each consisting of category, package and version field"""
    def printLine(cat, pack, ver):
        catlen = 25
        packlen = 25
        print cat + " " * ( catlen - len( cat ) ) + pack + " " * ( packlen - len( pack ) ) + ver

    printLine('Category', 'Package', 'Version')
    printLine('--------', '-------', '-------')
    for category, package, version in lines:
        if condition( category, package, version ):
            printLine(category, package, version)

def printInstallables():
    """get all the packages that can be installed"""
    def alwaysTrue( category, package, version ):
        return True
    printCategoriesPackagesAndVersions( PortageInstance.getInstallables(), alwaysTrue )

def printInstalled():
    """get all the packages that are already installed"""
    printCategoriesPackagesAndVersions( PortageInstance.getInstallables(), isInstalled )
    
    
def isInstalled( category, package, version, buildType='' ):
    # find in old style database
    path = etcDir()
    fileName = os.path.join(path,'installed')
    if not os.path.isfile( fileName ):
        return False

    found = False
    f = open( fileName, "rb" )
    for line in f.read().splitlines():
        (_category, _packageVersion) = line.split( "/" )
        (_package, _version) = packageSplit(_packageVersion)
        if category <> '' and version <> '' and category == _category and package == _package and version == _version:
            found = True
            break
        elif category == '' and version == '' and package == _package:
            found = True
            break
    f.close()

    # find in release mode database
    if not found and buildType <> '': 
        fileName = os.path.join(path,'installed-' + buildType )
        if os.path.isfile( fileName ):
            f = open( fileName, "rb" )
            for line in f.read().splitlines():
                (_category, _packageVersion) = line.split( "/" )
                (_package, _version) = packageSplit(_packageVersion)
                if category <> '' and version <> '' and category == _category and package == _package and version == _version:
                    found = True
                    break
                elif category == '' and version == '' and package == _package:
                    found = True
                    break
            f.close()

    if ( not found ):
        """ try to detect packages from the installer """
        bin = utils.checkManifestFile( os.path.join( os.getenv( "KDEROOT" ), "manifest", package + "-" + version + "-bin.ver"), category, package, version )
        lib = utils.checkManifestFile( os.path.join( os.getenv( "KDEROOT" ), "manifest", package + "-" + version + "-lib.ver"), category, package, version )
        found = found or bin or lib

    if ( not found and os.getenv( "EMERGE_VERSIONING" ) == "False" or os.getenv( "EMERGE_SOURCEONLY" ) == "True" ):
        """ check for any installation """
        if not os.path.exists(os.path.join( os.getenv( "KDEROOT" ), "manifest" ) ):
            return False
        if package.endswith( "-src" ):
            package = package[:-4]
        for filename in os.listdir( os.path.join( os.getenv( "KDEROOT" ), "manifest" ) ):
            if filename.startswith( package ):
                found = True
                break
    return found

def findInstalled( category, package, buildType='' ):
    fileName = os.path.join( etcDir(), "installed" )
    if ( not os.path.isfile( fileName ) ):
        return None

    ret = None
    f = open( fileName, "rb" )
    str = "^%s/%s-(.*)$" % ( category, re.escape(package) )
    regex = re.compile( str )
    for line in f.read().splitlines():
        match = regex.match( line )
        if match:
            utils.debug( "found: " + match.group(1), 2 )
            ret = match.group(1)
    f.close()
    return ret;

def addInstalled( category, package, version, buildType='' ):
    utils.debug( "addInstalled called", 2 )
    # write a line to etc/portage/installed,
    # that contains category/package-version
    path = os.path.join( etcDir() )
    if ( not os.path.isdir( path ) ):
        os.makedirs( path )
    if buildType <> '': 
        fileName = 'installed-' + buildType
    else:
        fileName = 'installed'
    utils.debug("installing package %s - %s into %s" % (package, version, fileName), 2)
    if( os.path.isfile( os.path.join( path, fileName ) ) ):
        f = open( os.path.join( path, fileName ), "rb" )
        for line in f:
            if line.startswith( "%s/%s-%s" % ( category, package, version) ):
                utils.warning( "version already installed" )
                return
            elif line.startswith( "%s/%s-" % ( category, package ) ):
                utils.die( "already installed, this should no happen" )
    f = open( os.path.join( path, fileName ), "ab" )
    f.write( "%s/%s-%s\r\n" % ( category, package, version ) )
    f.close()

def remInstalled( category, package, version, buildType='' ):
    utils.debug( "remInstalled called", 2 )
    if buildType <> '': 
        fileName = 'installed-' + buildType
    else:
        fileName = 'installed'
    utils.debug("removing package %s - %s from %s" % (package, version, fileName), 2)
    dbfile = os.path.join( etcDir(), fileName )
    tmpdbfile = os.path.join( etcDir(), "TMPinstalled" )
    found=False
    if os.path.exists( dbfile ):
        file = open( dbfile, "rb" )
        tfile = open( tmpdbfile, "wb" )
        for line in file:
            ## \todo the category should not be part of the search string 
            ## because otherwise it is not possible to unmerge package using 
            ## the same name but living in different categories
            if not line.startswith("%s/%s" % ( category, package ) ):
                tfile.write( line )
            else:
                found=True
        file.close()
        tfile.close()
        os.remove( dbfile )
        os.rename( tmpdbfile, dbfile )
    return found

def getPackagesCategories(packageName, defaultCategory = None):

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
        
            if PortageInstance.isCategory( defaultCategory ) and PortageInstance.isPackage( defaultCategory, packageName ):
                # prefer the default category
                packageList = [ packageName ]
                categoryList = [ defaultCategory ]
            else:
                if PortageInstance.getCategory( packageName ):
                    packageList = [ packageName ]
                    categoryList = [ PortageInstance.getCategory( packageName ) ]
                else:
                    utils.warning( "unknown category or package: %s" % packageName )
    elif len( packageName.split( "/" ) ) == 2:
        [ cat, pac ] = packageName.split( "/" )
        validPackage = False
        if PortageInstance.isCategory( cat ):
            categoryList = [ cat ]
        else:
            utils.warning( "unknown category %s; ignoring package %s" % ( cat, packageName ) )
        if len( categoryList ) > 0 and PortageInstance.isPackage( categoryList[0], pac ):
            packageList = [ pac ]
        if len( categoryList ) and len( packageList ):
            utils.debug( "added package %s/%s" % ( categoryList[0], pac ), 2 )
        else:
            utils.debug( "ignoring package %s" % packageName )
    else:
        utils.error( "unknown packageName" )

    return packageList, categoryList


