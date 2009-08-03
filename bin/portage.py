## @package portage 
#  @brief contains portage tree related functions
#  @note this file should replace all other related portage related files
import utils

import __builtin__
import imp
import os
import re
import sys

def __import__( module ):
    utils.debug( "module to import: %s" % module, 2 )
    if not os.path.isfile( module ):
        return __builtin__.__import__( module )
    else:
        sys.path.append( os.path.dirname( module ) )
        fileHdl = open( module )
        modulename = os.path.basename( module ).replace('.py', '')
        return imp.load_module( modulename.replace('.', '_'), fileHdl, module, imp.get_suffixes()[1] )

def rootDir():
    portageroot = os.getenv("EMERGE_PORTAGE_ROOT")
    if not portageroot == None:
        return portageroot
    else:
        return os.path.join( os.getenv( "KDEROOT" ), "emerge", "portage" )

def etcDir():
    return os.path.join( os.getenv( "KDEROOT" ), "etc", "portage" )

def getFilename( category, package, version ):
    """ return absolute filename for a given category, package and version"""
    file = os.path.join( rootDir(), category, package, "%s-%s.py" % ( package, version ) )
    return file

def getCategory( package ):
    """returns the category of this package"""
    utils.debug( "getCategory: %s" % package, 2 )
    basedir = rootDir()

    for cat in os.listdir( basedir ):
        #print "category:", cat
        catpath = os.path.join( basedir, cat )
        if ( os.path.isdir( catpath ) ):
            for pack in os.listdir( catpath ):
                #print "    package:", pack
                if ( pack == package ):
                    utils.debug( "found: category %s for package %s" % ( cat, pack ), 1 )
                    return cat
    return False

def isCategory( category ):
    if category in os.listdir( rootDir() ):
        catpath = os.path.join( rootDir(), category )
        utils.debug( "isCategory: catpath=%s" % catpath, 2 )
        if os.path.isdir( catpath ):
            return True
    return False

def isPackage( category, package ):
    return os.path.exists( os.path.join( rootDir(), category, package ) )

def getCategoryPackageVersion( path ):
    utils.debug( "getCategoryPackageVersion: %s" % path ,1 )
    ( head, file ) = os.path.split( path )
    ( head, package ) = os.path.split( head )
    ( head, category ) = os.path.split( head )

    (filename, ext) = os.path.splitext( file )
    ( package, version ) = packageSplit( filename )
    utils.debug( "category: %s, package: %s, version: %s" % ( category, package, version ), 1 )
    return [ category, package, version ]

def getAllPackages( category ):
    if isCategory( category ):
        plist = os.listdir( os.path.join( rootDir(), category ) )
        if ".svn" in plist: plist.remove( ".svn" )
        for entry in plist:
            if not os.path.isdir( os.path.join( rootDir(), category, entry ) ):
                plist.remove( entry )
        debug( plist, 2 )
        if os.path.exists( os.path.join( rootDir(), category, "dont_build.txt" ) ):
            f = open( os.path.join( rootDir(), category, "dont_build.txt" ), "r" )
            for line in f:
                try:
                    plist.remove( line.strip() )
                except:
                    utils.warning( "couldn't remove package %s from category %s's package list" % ( line.strip(), category ) )
        return plist
    else:
        return

def getPackageInstance( category, package ):
    """return instance of class Package from package file"""
    version = getNewestVersion( category, package )
    fileName = getFilename( category, package, version )
    module = __import__( fileName )
    p = module.Package()
    p.setup(fileName, category, package, version)
    return p
    
def getDefaultTarget( category, package, version ):
    """ """
    utils.debug( "importing file %s" % getFilename( category, package, version ), 1 )
    mod = __import__( getFilename( category, package, version ) )
    if hasattr( mod, 'subinfo' ):
        info = mod.subinfo()
        return mod.subinfo().defaultTarget
    else:
        return None

def getAllTags( category, package, version ):
    """ """
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

def getNewestVersion( category, package ):
    """
    returns the newest version of this category/package
    """
#    if verbose() >= 1:
#        print "getNewestVersion:", category, package
    if( category == None ):
        die("Empty category for package '%s'" % package )
    if category not in os.listdir( rootDir() ):
        die( "could not find category '%s'" % category )
    if package not in os.listdir( os.path.join( rootDir(), category ) ):
        die( "could not find package '%s' in category '%s'" % ( package, category ) )

    packagepath = os.path.join( rootDir(), category, package )

    versions = []
    for file in os.listdir( packagepath ):
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
    if os.path.isfile( getFilename( category, package, version ) ):
        f = open( getFilename( category, package, version ), "rb" )
    else:
        die( "package name %s/%s-%s unknown" % ( category, package, version ) )
    lines = f.read()
    #print "lines:", lines
    # get DEPENDS=... lines
    deplines = []
    inDepend = False

    utils.debug( "solving package: %s-%s" % ( package, version ), 2 )
    # FIXME make this more clever
    for line in lines.splitlines():
        if ( inDepend == True ):
            if ( line.find( "\"\"\"" ) != -1 ):
                break
            deplines.append( [ line, 'default' ] )
        if ( line.startswith( "DEPEND" ) ):
            inDepend = True
    if not len(deplines) > 0:
        utils.debug( "%s %s %s %s" % ( category, package, version, getFilename( category, package, version ) ), 2 )
        mod = __import__( getFilename( category, package, version ) )
        if hasattr( mod, 'subinfo' ):
            info = mod.subinfo()
            for line in info.hardDependencies.keys():
                deplines.append( [line, info.hardDependencies[ line ] ] )
                #warning( "%s %s" % (line, info.hardDependencies[ line ] ) )

#    if verbose() >= 1 and len( deplines ) > 0:
#        print "deplines:", deplines

    deps = []
    for line in deplines:
        if len(line) <= 1 or len(line[ 0 ]) <= 1:
            """if empty or if first argument is empty """
            continue
        (category, package) = line[ 0 ].split( "/" )
        version = getNewestVersion( category, package )
        deps.append( [ category, package, version, line[ 1 ] ] )
    return deps

def solveDependencies( category, package, version, deplist ):
    if ( category == "" ):
        category = getCategory( package )

    if ( version == "" ):
        version = getNewestVersion( category, package )

    tag = 1
    if ( tag == "" ):
        tag = getAllTags( category, package, version ).keys()[ 0 ]

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

def getInstallables():
    """get all the packages that are within the portage directory"""
    instList = list()
    catdirs = os.listdir( rootDir() )
    if '.svn' in catdirs:
        catdirs.remove( '.svn' )
    for category in catdirs:
        pakdirs = os.listdir( os.path.join( rootDir(), category ) )
        if '.svn' in pakdirs:
            pakdirs.remove( '.svn' )
        for package in pakdirs:
            if os.path.isdir( os.path.join( rootDir(), category, package ) ):
                scriptdirs = os.listdir( os.path.join( rootDir(), category, package ) )
                for script in scriptdirs:
                    if script.endswith( '.py' ):
                        version = script.replace('.py', '').replace(package + '-', '')
                        instList.append([category, package, version])
    return instList

def printTargets( category, package, version ):
    """ """
    targetsDict = getAllTags( category, package, version )
    defaultTarget = getDefaultTarget( category, package, version )
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
    utils.debug( "importing file %s" % getFilename( category, package, version ), 1 )
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
    printCategoriesPackagesAndVersions( getInstallables(), alwaysTrue )

def printInstalled():
    """get all the packages that are already installed"""
    printCategoriesPackagesAndVersions( getInstallables(), isInstalled )
    
    
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

    if ( not found and os.getenv( "EMERGE_VERSIONING" ) == "False" ):
        """ check for any installation """
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
    str = "^%s/%s-(.*)$" % ( category, package )
    regex = re.compile( str )
    for line in f.read().splitlines():
        match = regex.match( line )
        if match:
            utils.debug( "found: " + match.group(1), 2 )
            ret = match.group(1)
    f.close()
    return ret;

def addInstalled( category, package, version, buildType='' ):
    utils.debug( "addInstalled called", 1 )
    # write a line to etc/portage/installed,
    # that contains category/package-version
    path = os.path.join( etcDir() )
    if ( not os.path.isdir( path ) ):
        os.makedirs( path )
    if buildType <> '': 
        fileName = 'installed-' + buildType
    else:
        fileName = 'installed'
    if( os.path.isfile( os.path.join( path, fileName ) ) ):
        f = open( os.path.join( path, fileName ), "rb" )
        for line in f:
            # FIXME: this is not a good definition of a package entry
            if line.startswith( "%s/%s-" % ( category, package ) ):
                warning( "already installed" )
                return
    f = open( os.path.join( path, fileName ), "ab" )
    f.write( "%s/%s-%s\r\n" % ( category, package, version ) )
    f.close()

def remInstalled( category, package, version, buildType='' ):
    utils.debug( "remInstalled called", 1 )
    if buildType <> '': 
        fileName = 'installed-' + buildType
    else:
        fileName = 'installed'
    dbfile = os.path.join( etcDir(), fileName )
    tmpdbfile = os.path.join( etcDir(), "TMPinstalled" )
    if os.path.exists( dbfile ):
        file = open( dbfile, "rb" )
        tfile = open( tmpdbfile, "wb" )
        for line in file:
            if not line.startswith("%s/%s" % ( category, package ) ):
                tfile.write( line )
        file.close()
        tfile.close()
        os.remove( dbfile )
        os.rename( tmpdbfile, dbfile )
