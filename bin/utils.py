# this file contains some helper functions for emerge

# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>


import httplib
import ftplib
import os
import sys
import re
import urlparse
import shutil
import zipfile
import tarfile
import hashlib
import subprocess
import __builtin__
import imp
import info

import portage_versions


### fetch functions

#FIXME: get this from somewhere else:
if (os.getenv( "directory_layout" ) == "installer" ):
    WGetExecutable = os.path.join( os.getenv( "KDEROOT" ), "bin", "wget.exe" )
else:
    WGetExecutable = os.path.join( os.getenv( "KDEROOT" ), "gnuwin32", "bin", "wget.exe" )

def __import__( module ):
    if not os.path.isfile( module ):
        return __builtin__.__import__( module )
    else:
        sys.path.append( os.path.dirname( module ) )
        fileHdl=open( module )
        modulename=os.path.basename( module ).replace('.py', '')
        return imp.load_module( modulename.replace('.', '_'), fileHdl, module, imp.get_suffixes()[1] )

def test4application( appname, args=None ):
    try:
        f = file('NUL:')
        p = subprocess.Popen( appname, stdout=f, stderr=f )
        p.wait()
        return True
    except:
        if verbose() > 1:
            print "could not find application %s" % appname
        return False

def verbose():
    verb=os.getenv( "EMERGE_VERBOSE" )
    if ( not verb == None and verb.isdigit() and int(verb) > 0 ):
        return int( verb )
    else:
        return 0

def getFiles( urls, destdir ):
    if verbose() > 1:
        print "getfiles called. urls:", urls
    # make sure distfiles dir exists
    if ( not os.path.exists( destdir ) ):
        os.makedirs( destdir )

    for url in urls.split():
        #print "getfiles url:", url
        if ( not getFile( url, destdir ) ):
            return False

    return True

def getFile( url, destdir ):
    if verbose() > 1:
        print "getFile called. url:", url
    if url == "":
        error( "fetch: no url given" )
        return False


    wgetpath = WGetExecutable
    if ( os.path.exists( wgetpath ) ):
        return wgetFile( url, destdir )

    scheme, host, path, params, qu, fr = urlparse.urlparse( url )


    filename = os.path.basename( path )
    if verbose() > 0:
        print scheme
        print host
        print path
        print filename

    if ( scheme == "http" ):
        return getHttpFile( host, path, destdir, filename )
    elif ( scheme == "ftp" ):
        return getFtpFile( host, path, destdir, filename )
    else:
        error( "getFile: protocol not understood" )
        return False

def wgetFile( url, destdir ):
    compath = WGetExecutable
    command = "%s -c -t 1 -P %s %s" % ( compath, destdir, url )
    if verbose() > 1:
        print "wgetfile called"
        print "executing this command:", command
    attempts=1
    if url.lower().startswith("http://downloads.sourceforge.net"):
        if verbose() > 0:
            print "Detected downloads.sourceforge.net... Trying three times."
        attempts=3

    while(attempts > 0):
        attempts -= 1
        ret = system( command )
        if verbose() > 0:
            print "wget ret:", ret
        if ret == True:
            # success stop early.
            break;

    return ret

def getFtpFile( host, path, destdir, filename ):
    # FIXME check return values here (implement useful error handling)...
    if verbose() > 1:
        print "FIXME getFtpFile called.", host, path

    outfile = open( os.path.join( destdir, filename ), "wb" )
    ftp = ftplib.FTP( host )
    ftp.login( "anonymous", "johndoe" )
    ftp.retrbinary( "RETR " + path, outfile.write )

    outfile.close()
    return True

def getHttpFile( host, path, destdir, filename ):
    # FIXME check return values here (implement useful error handling)...
    if verbose() > 1:
        print "getHttpFile called.", host, path

    conn = httplib.HTTPConnection( host )
    conn.request( "GET", path )
    r1 = conn.getresponse()
    if verbose() > 0:
        print r1.status, r1.reason
        
    count = 0
    while r1.status == 302:
        if count > 10:
            print "Redirect loop"
            return False
        count += 1
        scheme, host, path, params, qu, fr = urlparse.urlparse( r1.getheader( "Location" ) )
        if verbose() > 1:
            print "Redirection.", host, path
        conn = httplib.HTTPConnection( host )
        conn.request( "GET", path )
        r1 = conn.getresponse()
        if verbose() > 0:
            print r1.status, r1.reason
    
        
    data = r1.read()

    f = open( os.path.join( destdir, filename ), "wb" )
    f.write( data )
    f.close()
    return True


### unpack functions

def unpackFiles( downloaddir, filenames, workdir ):
    cleanDirectory( workdir )

    for filename in filenames:
        if verbose() > 1:
            print "unpacking this file:", filename
        if ( not unpackFile( downloaddir, filename, workdir ) ):
            return False

    return True

def unpackFile( downloaddir, filename, workdir ):
    ( shortname, ext ) = os.path.splitext( filename )
    if ( ext == ".zip" ):
        return unZip( os.path.join( downloaddir, filename ), workdir )
    elif ( ext == ".gz" or ext == ".bz2" ):
        ( myshortname, myext ) = os.path.splitext( shortname )
        if ( myext == ".tar" ):
            return unTar( os.path.join( downloaddir, filename ), workdir )
        else:
            error( "unpacking %s" % myext )
            return False
    elif ( ext == ".exe" ):
        warning( "unpack ignoring exe file" )
        return True
    error( "dont know how to unpack this file: %s" % filename )
    return False

def unTar( file, destdir ):
    if verbose() > 1:
        print "unTar called. file: %s, destdir: %s" % ( file, destdir )
    ( shortname, ext ) = os.path.splitext( file )

    mode = "r"
    if ( ext == ".gz" ):
        mode = "r:gz"
    elif ( ext == ".bz2" ):
        mode = "r:bz2"

    tar = tarfile.open( file, mode )

    # FIXME how to handle errors here ?
    for foo in tar:
        tar.extract( foo, destdir )

    return True

def unZip( file, destdir ):
    if verbose() > 1:
        print "unZip called:", file, destdir

    if not os.path.exists(destdir):
        os.makedirs(destdir)

    zip = zipfile.ZipFile(file)

    for i, name in enumerate(zip.namelist()):
        if not name.endswith('/'):
            dirname = os.path.join( destdir, os.path.dirname( name ) )

            if not os.path.exists(dirname):
                os.makedirs(dirname)

            outfile = open(os.path.join(destdir, name), 'wb')
            outfile.write(zip.read(name))
            outfile.flush()
            outfile.close()

    return True


### svn fetch/unpack functions

def svnFetch( repo, destdir, username = None, password = None ):
    if verbose() > 1:
        print "utils svnfetch", repo, destdir
    if ( not os.path.exists( destdir ) ):
        os.makedirs( destdir )
    os.chdir( destdir )

    ret = 0
    #if ( len( os.listdir( destdir ) ) == 0 ):

    dir = os.path.basename( repo.replace( "/", "\\" ) )
    path = os.path.join( destdir, dir )
    if verbose() > 1:
        print "path: ", path 
    if ( not os.path.exists( path ) ):
        # not checked out yet
        command = "svn checkout %s" % repo
        if ( username != None ):
            command = command + " --username " + username
        if ( password != None ):
            command = command + " --password " + password
        if verbose() > 1:
            print "executing this:", command
        ret = system( command )
    else:
        # already checked out, so only update
        mode = "update"
        os.chdir( path )
        if verbose() > 1:
            print "svn up cwd:", os.getcwd()
        ret = system( "svn update" )

    if ( ret == 0 ):
        return True
    else:
        return False

### package dependencies functions

def isInstalled( category, package, version ):
    fileName = os.path.join( getEtcPortageDir(), "installed" )
    if ( not os.path.isfile( fileName ) ):
        warning( "installed db file does not exist" )
        return False

    found = False
    f = open( fileName, "rb" )
    for line in f.read().splitlines():
        if ( line == "%s/%s-%s" % ( category, package, version ) ):
            found = True
            break
    f.close()

    if ( not found ):
        """ try to detect packages from the installer """
        releasepack = os.path.join( os.getenv( "KDEROOT" ), "manifest", package + "-" + version + "-bin.mft" )
        develpack = os.path.join( os.getenv( "KDEROOT" ), "manifest", package + "-" + version + "-lib.mft" )
        if( os.path.isfile( releasepack ) or os.path.isfile( develpack ) ):
            found = True
    return found

def addInstalled( category, package, version ):
    if verbose() > 1:
        print "addInstalled called"
    # write a line to etc/portage/installed,
    # that contains category/package-version
    path = os.path.join( getEtcPortageDir() )
    if ( not os.path.isdir( path ) ):
        os.makedirs( path )
    if( os.path.isfile( os.path.join( path, "installed" ) ) ):
        f = open( os.path.join( path, "installed" ), "rb" )
        for line in f:
            # FIXME: this is not a good definition of a package entry
            if line.startswith( "%s/%s-" % ( category, package ) ):
                warning( "already installed" )
                return
    f = open( os.path.join( path, "installed" ), "ab" )
    f.write( "%s/%s-%s\r\n" % ( category, package, version ) )
    f.close()

def remInstalled( category, package, version ):
    if verbose() > 1:
        print "remInstalled called"
    dbfile = os.path.join( getEtcPortageDir(), "installed" )
    tmpdbfile = os.path.join( getEtcPortageDir(), "TMPinstalled" )
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

def getCategoryPackageVersion( path ):
    if verbose() > 1:
        print "getCategoryPackageVersion:", path
    ( head, file ) = os.path.split( path )
    ( head, package ) = os.path.split( head )
    ( head, category ) = os.path.split( head )

    (filename, ext) = os.path.splitext( file )
    ( package, version ) = packageSplit( filename )
    if verbose() > 1:
        print "category: %s, package: %s, version: %s" %( category, package, version )
    return [ category, package, version ]

def getPortageDir():
    return os.path.join( os.getenv( "KDEROOT" ), "emerge", "portage" )

def getEtcPortageDir():
    return os.path.join( os.getenv( "KDEROOT" ), "etc", "portage" )

def getFilename( category, package, version ):
    file = os.path.join( getPortageDir(), category, package, "%s-%s.py" % ( package, version ) )
    return file

def getCategory( package ):
    """
    returns the category of this package
    """
    if verbose() > 1:
        print "getCategory:", package
    basedir = getPortageDir()

    for cat in os.listdir( basedir ):
        #print "category:", cat
        catpath = os.path.join( basedir, cat )
        if ( os.path.isdir( catpath ) ):
            for pack in os.listdir( catpath ):
                #print "    package:", pack
                if ( pack == package ):
                    if verbose() > 1:
                        print "found:", cat, pack
                    return cat

def getAllTags( category, package, version ):
    """ """
    if hasattr( mod, 'subinfo' ):
        info = mod.subinfo()
        mod = __import__( getFilename( category, package, version ) )
        info = mod.subinfo()
        return info.svnTargets
    else:
        return dict()

def getNewestVersion( category, package ):
    """
    returns the newest version of this category/package
    """
#    if utils.verbose() >= 1:
#        print "getNewestVersion:", category, package
    if( category == None ):
        die("Empty category for package '%s'" % package )
    if category not in os.listdir( getPortageDir() ):
        die( "could not find category '%s'" % category )
    if package not in os.listdir( os.path.join( getPortageDir(), category ) ):
        die( "could not find package '%s' in category '%s'" % ( package, category ) )

    packagepath = os.path.join( getPortageDir(), category, package )

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

    if verbose() > 2:
        print "solving package: %s-%s" % ( package, version )
    # FIXME make this more clever
    for line in lines.splitlines():
        if ( inDepend == True ):
            if ( line.find( "\"\"\"" ) != -1 ):
                break
            deplines.append( [ line, 'default' ] )
        if ( line.startswith( "DEPEND" ) ):
            inDepend = True
    if not len(deplines) > 0:
        mod = __import__( getFilename( category, package, version ) )
        if hasattr( mod, 'subinfo' ):
            info = mod.subinfo()
            for line in info.hardDependencies.keys():
                deplines.append( [line, info.hardDependencies[ line ] ] )
                #warning( "%s %s" % (line, info.hardDependencies[ line ] ) )

#    if utils.verbose() >= 1 and len( deplines ) > 0:
#        print "deplines:", deplines

    deps = []
    for line in deplines:
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
#    if utils.verbose() >= 1:
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
    catdirs = os.listdir( getPortageDir() )
    if '.svn' in catdirs:
        catdirs.remove( '.svn' )
    for category in catdirs:
        pakdirs = os.listdir( os.path.join( getPortageDir(), category ) )
        if '.svn' in pakdirs:
            pakdirs.remove( '.svn' )
        for package in pakdirs:
            if os.path.isdir( os.path.join( getPortageDir(), category, package ) ):
                scriptdirs = os.listdir( os.path.join( getPortageDir(), category, package ) )
                for script in scriptdirs:
                    if script.endswith( '.py' ):
                        version = script.replace('.py', '').replace(package + '-', '')
                        instList.append([category, package, version])
    return instList

def printTargets( category, package, version ):
    """ """
    if verbose() > 1:
        print "importing file %s" % getFilename( category, package, version )
    mod = __import__( getFilename( category, package, version ) )
    packageInfo = mod.subinfo()
    svnTargetsList = packageInfo.svnTargets.keys()
    if not packageInfo.svnTargets['svnHEAD']:
        svnTargetsList.remove('svnHEAD')
    for i in svnTargetsList:
        if packageInfo.defaultTarget == i:
            print '*',
        else:
            print ' ',
        print i
    for i in packageInfo.targets.keys():
        if packageInfo.defaultTarget == i:
            print '*',
        else:
            print ' ',
        print i

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

def info( message ):
    if verbose() > 0:
        print "emerge info: %s" % message
    return True

def debug( message, level = 0 ):
    if verbose() > level:
        print "emerge debug: %s" % message
    return True

def warning( message ):
    if verbose() > 0:
        print "emerge warning: %s" % message
    return True

def error( message ):
    if verbose() > 0:
        print "emerge error: %s" % message
    return False

def die( message ):
    print "emerge fatal error: %s" % message
    exit( 1 )

def system( cmdstring ):
    if verbose() == 0:
        sys.stderr = file('test.outlog', 'wb')
        sys.stdout = sys.stderr
    p = subprocess.Popen( cmdstring, shell=True, stdout=sys.stdout, stderr=sys.stderr )
    ret = p.wait()
    return ( ret == 0 )

def copySrcDirToDestDir( srcdir, destdir ):
    if verbose() > 1:
        print "copySrcDirToDestDir called. srcdir: %s, destdir: %s" % ( srcdir, destdir )

    if ( not srcdir.endswith( "\\" ) ):
        srcdir += "\\"
    if ( not destdir.endswith( "\\" ) ):
        destdir += "\\"

    for root, dirs, files in os.walk( srcdir ):
        # do not copy files under .svn directories, because they are write-protected
        # and the they cannot easily be deleted...
        if ( root.find( ".svn" ) == -1 ):
            tmpdir = root.replace( srcdir, destdir )
            if ( not os.path.exists( tmpdir ) ):
                os.makedirs( tmpdir )
            for file in files:
                shutil.copy( os.path.join( root, file ), tmpdir )

def moveSrcDirToDestDir( srcdir, destdir ):
    if verbose() > 1:
        print "moveSrcDirToDestDir called. srcdir: %s, destdir: %s" % ( srcdir, destdir )
    shutil.move( srcdir, destdir )

def unmerge( rootdir, package, forced = False ):
    """ delete files according to the manifest files """
    if verbose() > 1:
        print "unmerge called: %s" % ( package )

    if os.path.exists( os.path.join( rootdir, "manifest"  ) ):
        for file in os.listdir( os.path.join( rootdir, "manifest" ) ):
            if file.endswith(".mft"):
                [ pkg, version ] = packageSplit( file.replace( ".mft", "" ) )
            if file.endswith( ".mft" ) and package==pkg:
                fptr = open( os.path.join( rootdir, "manifest", file ), 'rb' )
                for line in fptr:
                    line = line.replace( "\n", "" ).replace( "\r", "" )
                    if not line.find( " " ) == -1:
                        [ a, b ] = line.split( " ", 2 )
                    else:
                        a, b = line, ""
                    if os.path.join( rootdir, "manifest", file ) == os.path.join( rootdir, os.path.normcase( a ) ):
                        continue
                    if os.path.isfile( os.path.join( rootdir, os.path.normcase( a ) ) ):
                        hash = digestFile( os.path.join( rootdir, os.path.normcase( a ) ) )
                        if b == "" or hash == b:
                            if verbose() > 0:
                                print "deleting file %s" % a
                            os.remove( os.path.join( rootdir, os.path.normcase( a ) ) )
                        else:
                            warning( "file %s has different hash: %s %s, run with option --forced to delete it anyway" % ( os.path.normcase( a ), hash, b ) )
                            if forced:
                                os.remove( os.path.join( rootdir, os.path.normcase( a ) ) )
                    elif not os.path.isdir( os.path.join( rootdir, os.path.normcase( a ) ) ):
                        warning( "file %s is not existing" % ( os.path.normcase( a ) ) )
                fptr.close()
                os.remove( os.path.join( rootdir, "manifest", file ) )
    return

def manifestDir( srcdir, imagedir, package, version ):
    """ make the manifest files for an imagedir like the kdewin-packager does """
    if verbose() > 1:
        print "manifestDir called: %s %s" % ( srcdir, imagedir )

    if os.path.exists( os.path.join( imagedir, "manifest"  ) ):
        for file in os.listdir( os.path.join( imagedir, "manifest"  ) ):
            if file.startswith( package ):
                warning( "found package %s according to file '%s', .mft files will not be generated." % ( package, file ) )
                return

    myimagedir = imagedir
    if ( not imagedir.endswith( "\\" ) ):
        myimagedir = myimagedir + "\\"

    binList = list()
    libList = list()
    docList = list()
    dirType=0

    for root, dirs, files in os.walk( imagedir ):
        relativeRoot = root.replace( imagedir, "" )
        if relativeRoot.startswith( "\\bin" ):
            dirType=1
        elif relativeRoot.startswith( "\\lib" ):
            dirType=2
        elif relativeRoot.startswith( "\\share" ):
            dirType=3
        elif relativeRoot.startswith( "\\data" ):
            dirType=4
        elif relativeRoot.startswith( "\\etc" ):
            dirType=5
        elif relativeRoot.startswith( "\\include" ):
            dirType=6
        elif relativeRoot.startswith( "\\doc" ):
            dirType=7
        elif relativeRoot.startswith( "\\man" ) and not relativeRoot.startswith("\\manifest"):
            dirType=8
        else:
            dirType=1

        for file in files:
            if dirType == 1 or dirType == 2:
                if file.endswith( ".exe" ) or file.endswith( ".bat" ) or file.endswith( ".dll" ):
                    binList.append( os.path.join( root, file ).replace( myimagedir, "" ) )
            if dirType == 2:
                if file.endswith( ".a" ) or file.endswith( ".lib" ):
                    libList.append( os.path.join( root, file ).replace( myimagedir, "" ) )
            if dirType == 3 or dirType == 4 or dirType == 5:
                binList.append( os.path.join( root, file ).replace( myimagedir, "" ) )
            if dirType == 6:
                libList.append( os.path.join( root, file ).replace( myimagedir, "" ) )
            if dirType == 7 or dirType == 8:
                docList.append( os.path.join( root, file ).replace( myimagedir, "" ) )

    if not os.path.exists( os.path.join( imagedir, "manifest" ) ):
        os.mkdir( os.path.join( imagedir, "manifest" ) )

    if len(binList) > 0:
        binmanifest = open( os.path.join( imagedir, "manifest", "%s-%s-bin.mft" % ( package, version )), 'wb' )
    if len(libList) > 0:
        libmanifest = open( os.path.join( imagedir, "manifest", "%s-%s-lib.mft" % ( package, version )), 'wb' )
    if len(docList) > 0:
        docmanifest = open( os.path.join( imagedir, "manifest", "%s-%s-doc.mft" % ( package, version )), 'wb' )
#    if utils.verbose() >= 1:
#        print "bin: ", binList
#        print "lib: ", libList
#        print "doc: ", docList
    for file in binList:
        binmanifest.write( "%s %s\n" % ( file, digestFile( os.path.join( myimagedir, file ) ) ) )
    for file in libList:
        libmanifest.write( "%s %s\n" % ( file, digestFile( os.path.join( myimagedir, file )) ) )
    for file in docList:
        docmanifest.write( "%s %s\n" % ( file, digestFile( os.path.join( myimagedir, file ) ) ) )
            #print os.path.join( root, file ).replace( myimagedir, "" ), dig.hexdigest()
    if len(binList) > 0:
        binmanifest.write( os.path.join( "manifest", "%s-%s-bin.mft\n" % ( package, version ) ) )
        binmanifest.write( os.path.join( "manifest", "%s-%s-bin.ver\n" % ( package, version ) ) )
    if len(libList) > 0:
        libmanifest.write( os.path.join( "manifest", "%s-%s-lib.mft\n" % ( package, version ) ) )
        libmanifest.write( os.path.join( "manifest", "%s-%s-lib.ver\n" % ( package, version ) ) )
    if len(docList) > 0:
        docmanifest.write( os.path.join( "manifest", "%s-%s-doc.mft\n" % ( package, version ) ) )
        docmanifest.write( os.path.join( "manifest", "%s-%s-doc.ver\n" % ( package, version ) ) )

    if len(binList) > 0:
        binversion = open( os.path.join( imagedir, "manifest", "%s-%s-bin.ver" % ( package, version )), 'wb' )
    if len(libList) > 0:
        libversion = open( os.path.join( imagedir, "manifest", "%s-%s-lib.ver" % ( package, version )), 'wb' )
    if len(docList) > 0:
        docversion = open( os.path.join( imagedir, "manifest", "%s-%s-doc.ver" % ( package, version )), 'wb' )
    if len(binList) > 0:
        binversion.write( "%s %s Binaries\n%s:" % ( package, version, package ) )
    if len(libList) > 0:
        libversion.write( "%s %s developer files\n%s:" % ( package, version, package ) )
    if len(docList) > 0:
        docversion.write( "%s %s Documentation\n%s:" % ( package, version, package ) )

def mergeImageDirToRootDir( imagedir, rootdir ):
    copySrcDirToDestDir( imagedir, rootdir )

def moveEntries( srcdir, destdir ):
    for entry in os.listdir( srcdir ):
        #print "rootdir:", root
        if verbose() > 1:
            print "entry:", entry
        src = os.path.join( srcdir, entry )
        dest = os.path.join( destdir, entry )
        if verbose() > 1:
            print "src: %s dest: %s" %( src, dest )
        if( os.path.isfile( dest ) ):
          os.remove( dest )
        if( os.path.isdir( dest ) ):
          continue
        os.rename( src, dest )

def moveImageDirContents( imagedir, relSrcDir, relDestDir ):
    srcdir = os.path.join( imagedir, relSrcDir )
    destdir = os.path.join( imagedir, relDestDir )    

    if ( not os.path.isdir( destdir ) ):
        os.mkdir( destdir )

    moveEntries( srcdir, destdir )
    os.chdir( imagedir )    
    os.removedirs( relSrcDir )

def fixCmakeImageDir( imagedir, rootdir ):
    """
    when using DESTDIR=foo under windows, it does not _replace_
    CMAKE_INSTALL_PREFIX with it, but prepends destdir to it.
    so when we want to be able to install imagedir into KDEROOT,
    we have to move things around...
    """
    if verbose() > 1:
        print "fixImageDir:", imagedir, rootdir
    # imagedir = e:\foo\thirdroot\tmp\dbus-0\image
    # rootdir  = e:\foo\thirdroot
    # files are installed to
    # e:\foo\thirdroot\tmp\dbus-0\image\foo\thirdroot
    ( rootdrive, rootpath ) = os.path.splitdrive( rootdir )
    #print "rp:", rootpath
    if ( rootpath.startswith( "\\" ) ):
        rootpath = rootpath[1:]
    tmp = os.path.join( imagedir, rootpath )
    if verbose() > 1:
        print "tmp:", tmp
    tmpdir = os.path.join( imagedir, "tMpDiR" )

    if ( not os.path.isdir( tmpdir ) ):
        os.mkdir( tmpdir )

    moveEntries( tmp, tmpdir )
    os.chdir( imagedir )    
    os.removedirs( rootpath )
    moveEntries( tmpdir, imagedir )
    cleanDirectory( tmpdir )
    os.rmdir( tmpdir )

def cleanDirectory( dir ):
    if ( os.path.exists( dir ) ):
        for root, dirs, files in os.walk( dir, topdown=False):
            for name in files:
                try:
                    os.remove( os.path.join(root, name) )
                except:
                    die( "couldn't delete file %s\n ( %s )" % ( name, os.path.join( root, name ) ) )
            for name in dirs:
                try:
                    os.rmdir( os.path.join(root, name) )
                except:
                    die( "couldn't delete directory %s\n( %s )" % ( name, os.path.join( root, name ) ) )
    else:
      os.makedirs( dir )

def sedFile( directory, file, sedcommand ):
    """ runs the given sed command on the given file """
    os.chdir( directory )
    backup = "%s.orig" % file
    if( os.path.isfile( backup ) ):
        os.remove( backup )

    os.rename( file, backup )

    command = "type %s | sed %s > %s" % ( backup, sedcommand, file )
    if verbose() > 1:
        print "sedFile command:", command

    system( command ) or die( "utils sedFile failed" )

def digestFile( filepath ):
    """ md5-digests a file """
    hash = hashlib.md5()
    file = open( filepath, "rb" )
    for line in file:
        hash.update( line )
    file.close()
    return hash.hexdigest()

def toMSysPath( path ):
    path = path.replace( '\\', '/' )
    if ( path[1] == ':' ):
      path = '/' + path[0].lower() + '/' + path[3:]
    return path
