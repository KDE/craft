# -*- coding: utf-8 -*-
"""@brief utilities
this file contains some helper functions for emerge
"""

# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>
# Ralf Habacker <ralf.habacker [AT] freenet [DOT] de>

import http.client
import ftplib
import urllib.parse
import shutil
import zipfile
import tarfile
import hashlib
import traceback
import tempfile
import getpass
import subprocess
import re
import inspect
import datetime
from operator import itemgetter
import ctypes

import Notifier.NotificationLoader
from emerge_config import *
from emerge_config import etcPortageDir


if os.name == 'nt':
    import msvcrt # pylint: disable=F0401
else:
    import fcntl # pylint: disable=F0401

import configparser

def abstract():
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + ' must be implemented in subclass')

def getCallerFilename():
    """ returns the file name of the """
    filename = None
    try:
        frame=inspect.currentframe()
        count = 2
        while count > 0 and frame:
            frame = frame.f_back
            # python 3.3 includes unnecessary importlib frames, skip them
            if frame and frame.f_code.co_filename != '<frozen importlib._bootstrap>':
                count -= 1
    finally:
        if frame:
            filename = frame.f_code.co_filename
            del frame
    return filename

def varAsBool(var):
    return var.lower() in ['true', '1']


### fetch functions

#FIXME: get this from somewhere else:
WGetExecutable = os.path.join( emergeRoot(), "bin", "wget.exe" )
if not os.path.exists( WGetExecutable ):
    WGetExecutable = os.path.join( emergeRoot(), "dev-utils", "bin", "wget.exe" )

def test4application( appname):
    """check if the application specified by 'appname' is available"""
    try:
        f = open('NUL:')
        p = subprocess.Popen( appname, stdout=f, stderr=f )
        p.wait()
        return True
    except OSError:
        debug( "could not find application %s" % appname, 1 )
        return False

class Verbose(object):
    """
        This class will work on the overall output verbosity
        It defines the interface for the option parser but before the default
        value is taken from the environment variable.
        There is only one verbosity value for all parts of emerge.
        Always updates the shell variable EMERGE_VERBOSE.
    """
    __level = 1

    @staticmethod
    def increase():
        """increase verbosity"""
        Verbose.setLevel(Verbose.__level + 1)

    @staticmethod
    def decrease():
        """decrease verbosity"""
        Verbose.setLevel(Verbose.__level - 1)

    @staticmethod
    def level():
        return Verbose.__level

    @staticmethod
    def setLevel(newLevel):
        """ set the level by hand for quick and dirty changes """
        Verbose.__level = max(0, newLevel)

    def verbose( self ):
        """ returns the verbosity level for the application """
        return Verbose.__level

class TemporaryVerbosity(object):
    """Context handler for temporarily different verbosity"""
    def __init__(self, tempLevel):
        self.prevLevel = verbose()
        setVerbose(tempLevel)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trback):
        setVerbose(self.prevLevel)


def verbose():
    """return the value of the verbose level"""
    return Verbose.level()

def setVerbose( _verbose ):
    Verbose.setLevel(_verbose)

def getFiles( urls, destdir, suffix='' , filenames = ''):
    """download files from 'url' into 'destdir'"""
    debug( "getfiles called. urls: %s, filenames: %s, suffix: %s" % ( urls, filenames, suffix ), 1 )
    # make sure distfiles dir exists
    if ( not os.path.exists( destdir ) ):
        os.makedirs( destdir )

    if type(urls) == list:
        urlList = urls
    else:
        urlList = urls.split()

    if filenames == '':
        filenames = [ os.path.basename(x) for x in urlList ]

    if type(filenames) == list:
        filenameList = filenames
    else:
        filenameList = filenames.split()
        
    dlist = list(zip( urlList , filenameList ))
    
    for url,filename in dlist:
        if ( not getFile( url + suffix, destdir , filename ) ):
            return False

    return True

def getFile( url, destdir , filename='' ):
    """download file from 'url' into 'destdir'"""
    debug( "getFile called. url: %s" % url, 1 )
    if url == "":
        error( "fetch: no url given" )
        return False


    wgetpath = WGetExecutable
    if ( os.path.exists( wgetpath ) ):
        return wgetFile( url, destdir , filename )

    scheme, host, path, _, _, _ = urllib.parse.urlparse( url )


    filename = os.path.basename( path )
    debug( "%s\n%s\n%s\n%s" % ( scheme, host, path, filename ) )

    if ( scheme == "http" ):
        return getHttpFile( host, path, destdir, filename )
    elif ( scheme == "ftp" ):
        return getFtpFile( host, path, destdir, filename )
    else:
        error( "getFile: protocol not understood" )
        return False

def wgetFile( url, destdir, filename=''):
    """download file with wget from 'url' into 'destdir', if filename is given to the file specified"""
    compath = WGetExecutable
    command = "%s --no-check-certificate -c -t 10" % compath
    if varAsBool( emergeSettings.get("General", "EMERGE_NO_PASSIVE_FTP", "False")):
        command += " --no-passive-ftp "
    if(filename ==''):
        command += "  -P %s" % destdir
    else:
        command += " -O %s" % os.path.join( destdir, filename )
    command += " %s" % url
    debug( "wgetfile called", 1 )
    ret = system( command )
    debug( "wget ret: %s" % ret, 2)
    return ret

def getFtpFile( host, path, destdir, filename ):
    """download file from a ftp host specified by 'host' and 'path' into 'destdir' using 'filename' as file name"""
    # FIXME check return values here (implement useful error handling)...
    debug( "FIXME getFtpFile called. %s %s" % ( host, path ), 1 )

    ftp = ftplib.FTP( host )
    ftp.login( "anonymous", "johndoe" )
    with open( os.path.join( destdir, filename ), "wb" ) as outfile:
        ftp.retrbinary( "RETR " + path, outfile.write )

    return True

def getHttpFile( host, path, destdir, filename ):
    """download file from a http host specified by 'host' and 'path' into 'destdir' using 'filename' as file name"""
    # FIXME check return values here (implement useful error handling)...
    debug( "getHttpFile called. %s %s" % ( host, path ), 1 )

    conn = http.client.HTTPConnection( host )
    conn.request( "GET", path )
    r1 = conn.getresponse()
    debug( "status: %s; reason: %s" % ( str( r1.status ), str( r1.reason ) ) )

    count = 0
    while r1.status == 302:
        if count > 10:
            debug( "Redirect loop" )
            return False
        count += 1
        _, host, path, _, _, _ = urllib.parse.urlparse( r1.getheader( "Location" ) )
        debug( "Redirection: %s %s" % ( host, path ), 1 )
        conn = http.client.HTTPConnection( host )
        conn.request( "GET", path )
        r1 = conn.getresponse()
        debug( "status: %s; reason: %s" % ( str( r1.status ), str( r1.reason ) ) )


    data = r1.read()

    with open( os.path.join( destdir, filename ), "wb" ) as f:
        f.write( data )
    return True

def isCrEol(filename):
    with open(filename, "rb") as f:
        return str(f.readline(),'UTF-8').endswith("\r\n")

def checkFilesDigests( downloaddir, filenames, digests=None ):
    """check digest of (multiple) files specified by 'filenames' from 'downloaddir'"""
    if digests != None:
        if type(digests) == list:
            digestList = digests
        elif digests.find("\n") != -1:
            digestList = digests.splitLines()
        else:
            digestList = [digests]

    i = 0
    for filename in filenames:
        debug( "checking digest of: %s" % filename, 1 )
        pathName = os.path.join( downloaddir, filename )
        if digests == None:
            digestFileName = pathName + '.sha1'
            if not os.path.exists( digestFileName ):
                digestFileName, _ = os.path.splitext( pathName )
                digestFileName += '.sha1'
                if not os.path.exists( digestFileName ):
                    error( "digest validation request for file %s, but no digest  file present" %
                            pathName )
                    return False
            currentHash = digestFileSha1( pathName )
            with open( digestFileName, "r" ) as f:
                line = f.readline()
            digest = re.search('\\b[0-9a-fA-F]{40}\\b', line)
            if not digest:
                error( " digestFile %s for file %s does not contain a valid SHA1 hash" % (digestFileName,
                        pathName,) )
                return False
            digest = digest.group(0)
            if len(digest) != len(currentHash) or digest.find(currentHash) == -1:
                error( "SHA1 hash for file %s (%s) does not match (%s)" % (pathName, currentHash, digest) )
                return False
        # digest provided in digests parameter
        else:
            currentHash = digestFileSha1( pathName )
            digest = digestList[i].strip()
            if len(digest) != len(currentHash) or digest.find(currentHash) == -1:
                error( "SHA1 hash for file %s (%s) does not match (%s)" % (pathName, currentHash, digest) )
                return False
        i = i + 1
    return True


def createFilesDigests( downloaddir, filenames ):
    """create digests of (multiple) files specified by 'filenames' from 'downloaddir'"""
    digestList = list()
    for filename in filenames:
        pathName = os.path.join( downloaddir, filename )
        digest = digestFileSha1( pathName )
        entry = filename, digest
        digestList.append(entry)
    return digestList
    
def createDigestFile(path):
    """creates a sha1 diget file"""
    digets = digestFileSha1(path)
    f = open(path + ".sha1","wb+")
    f.write(bytes(digets,"UTF-8"))
    f.write(bytes("\n",'UTF-8'))
    f.close()

def printFilesDigests( digestFiles, buildTarget=None):
    size = len( digestFiles )
    i = 0
    for (fileName, digest) in digestFiles:
        print("%40s %s" % ( fileName, digest ), end=' ')
        if size == 1:
            if buildTarget == None:
                print("      '%s'" % ( digest ))
            else:
                print("self.targetDigests['%s'] = '%s'" % ( buildTarget, digest ))
        else:
            if buildTarget == None:
                if i == 0:
                    print("      ['%s'," % ( digest ))
                elif i == size-1:
                    print("       '%s']" % ( digest ))
                else:
                    print("       '%s'," % ( digest ))
                i = i + 1
            else:
                if i == 0:
                    print("self.targetDigests['%s'] = ['%s'," % ( buildTarget, digest ))
                elif i == size-1:
                    print("                             '%s']" % ( digest ))
                else:
                    print("                             '%s'," % ( digest ))
                i = i + 1

### unpack functions

def unpackFiles( downloaddir, filenames, workdir ):
    """unpack (multiple) files specified by 'filenames' from 'downloaddir' into 'workdir'"""
    cleanDirectory( workdir )

    for filename in filenames:
        debug( "unpacking this file: %s" % filename, 1 )
        if ( not unpackFile( downloaddir, filename, workdir ) ):
            return False

    return True

def unpackFile( downloaddir, filename, workdir ):
    """unpack file specified by 'filename' from 'downloaddir' into 'workdir'"""
    ( shortname, ext ) = os.path.splitext( filename )
    if ( ext == ".zip" ):
        return unZip( os.path.join( downloaddir, filename ), workdir )
    elif ( ext == ".7z" ):
        return un7zip( os.path.join( downloaddir, filename ), workdir )
    elif ( ext == ".tgz" ):
        return unTar( os.path.join( downloaddir, filename ), workdir )
    elif ( ext == ".gz" or ext == ".bz2" or ext == ".lzma" or ext == ".xz" ):
        _, myext = os.path.splitext( shortname )
        if ( myext == ".tar" ):
            return unTar( os.path.join( downloaddir, filename ), workdir )
        else:
            error( "unpacking %s" % myext )
            return False
    elif ( ext == ".exe" ):
        warning( "unpack ignoring exe file" )
        return True
    else:
        error( "dont know how to unpack this file: %s" % filename )
    return False

def un7zip( fileName, destdir ):
    command = "7za x -r -y -o%s %s" % ( destdir, fileName )
    if verbose() > 1:
        return system( command )
    else:
        tmp = tempfile.TemporaryFile()
        return system( command, stdout=tmp )

def unTar( fileName, destdir ):
    """unpack tar file specified by 'file' into 'destdir'"""
    debug( "unTar called. file: %s, destdir: %s" % ( fileName, destdir ), 1 )
    ( shortname, ext ) = os.path.splitext( fileName )
    emerge_tmp = os.path.join(destdir,"emerge_tmp")

    mode = "r"
    if ( ext == ".gz" ):
        mode = "r:gz"
    #elif(ext == ".bz2"):
        #mode = "r:bz2"
    elif(ext == ".lzma" or ext == ".xz" or ext == ".bz2"):
        un7zip( fileName, emerge_tmp )
        _, tarname = os.path.split( shortname )
        fileName = os.path.join( emerge_tmp , tarname )


    if not os.path.exists( fileName ):
        error( "couldn't find file %s" % fileName )
        return False

    try:
        with tarfile.open( fileName, mode ) as tar:
        # FIXME how to handle errors here ?
            for tarMember in tar:
                try:
                    if tarMember.issym():
                        tarDir = os.path.dirname(tarMember.name)
                        target = tarMember.linkname
                        if not target.startswith("/"):#abspath?
                            target = os.path.normpath("%s/%s"%(tarDir, target)).replace("\\","/")
                        if target in tar.getnames():
                            tar.extract(target, emerge_tmp )
                            shutil.move(os.path.join( emerge_tmp , tarDir , tarMember.linkname ),os.path.join( destdir , tarMember.name ))
                            warning("Resolved symlink %s in tarfile %s to %s" % ( tarMember.name, fileName , tarMember.linkname))
                        else:
                            warning("link target %s for %s not included in tarfile" % ( target , tarMember.name))
                    else:
                        tar.extract(tarMember, destdir )
                except tarfile.TarError:
                    error( "couldn't extract file %s to directory %s" % ( fileName, destdir ) )
                    return False
                except IOError:
                    warning("Failed to extract %s to directory %s" % ( tarMember.name, destdir ) )
        return True
    except tarfile.TarError:
        error( "could not open existing tar archive: %s" % fileName )
        return False
    finally:
        if os.path.exists(emerge_tmp):
            shutil.rmtree(emerge_tmp)

def unZip( fileName, destdir ):
    """unzip file specified by 'file' into 'destdir'"""
    debug( "unZip called: file %s to destination %s" % ( fileName, destdir ), 1 )

    if not os.path.exists( destdir ):
        os.makedirs( destdir )

    try:
        zipObj = zipfile.ZipFile( fileName )
    except (zipfile.BadZipfile, IOError):
        error( "couldn't extract file %s" % fileName )
        return False

    for name in zipObj.namelist():
        if not name.endswith( '/' ):
            dirname = os.path.join( destdir, os.path.dirname( name ) )

            if not os.path.exists( dirname ):
                os.makedirs( dirname )

            with open( os.path.join( destdir, name ), 'wb' ) as outfile:
                outfile.write( zipObj.read( name ) )

    return True


def info( message ):
    if verbose() > 0:
        print("emerge info: %s" % message)
    return True

def debug( message, level=0 ):
    if verbose() > level and verbose() > 0:
        print("emerge debug:", message)
    sys.stdout.flush()
    return True

def warning( message ):
    if verbose() > 0:
        try:
            print("emerge warning: %s" % message)
        except UnicodeEncodeError:
            print("emerge warning: failed to print message")
    return True

def new_line( level=0 ):
    if verbose() > level and verbose() > 0:
        print()

def debug_line( level=0 ):
    if verbose() > level and verbose() > 0:
        print("_" * 80)

def error( message ):
    if verbose() > 0:
        print("emerge error: %s" % message, file=sys.stderr)
    return False

def die( message ):
    print("emerge fatal error: %s" % message, file=sys.stderr)
    stopAllTimer()
    exit( 1 )

def traceMode():
    """return the value of the trace level"""
    return emergeSettings.args.trace

def trace( message, dummyLevel=0 ):
    if traceMode(): #> level:
        print("emerge trace:", message)
    sys.stdout.flush()
    return True

def system(cmd, **kw ):
    """execute cmd in a shell. All keywords are passed to Popen. stdout and stderr
    might be changed depending on the chosen logging options."""
    kw['shell'] = True
    return systemWithoutShell(cmd, **kw)

def systemWithoutShell(cmd, **kw):
    """execute cmd. All keywords are passed to Popen. stdout and stderr
    might be changed depending on the chosen logging options."""

    debug( "executing command: %s" % cmd, 1 )

    if kw.get('stdout') is None:
        kw['stdout'] = sys.stdout
    if kw.get('stderr') is None:
        kw['stderr'] = sys.stderr

    redirected = False
    prevStreams = sys.stdout,  sys.stderr
    try:
        if verbose() == 0 and kw['stdout']== sys.stdout and kw['stderr'] == sys.stderr:
            redirected = True
            sys.stderr = sys.stdout = open('test.outlog', 'wb')
        p = subprocess.Popen( cmd, **kw )
        ret = p.wait()
    finally:
        if redirected:
            sys.stderr.close()
            sys.stdout,  sys.stderr = prevStreams

    return ( ret == 0 )

def copySrcDirToDestDir( srcdir, destdir ):
    """ deprecated """
    return copyDir( srcdir, destdir )

def moveSrcDirToDestDir( srcdir, destdir ):
    """ deprecated """
    return moveDir( srcdir, destdir )

def getFileListFromDirectory( imagedir ):
    """ create a file list containing hashes """
    ret = []

    myimagedir = imagedir
    if ( not imagedir.endswith( "\\" ) ):
        myimagedir = myimagedir + "\\"

    for root, _, files in os.walk( imagedir ):
        for fileName in files:
            ret.append( ( os.path.join( root, fileName ).replace( myimagedir, "" ), digestFile( os.path.join( root, fileName ) ) ) )
    return ret


def unmergeFileList(rootdir, fileList, forced=False):
    """ delete files in the fileList if has matches or forced is True """
    for filename, filehash in fileList:
        fullPath = os.path.join(rootdir, os.path.normcase( filename))
        if os.path.isfile(fullPath):
            currentHash = digestFile(fullPath)
            if currentHash == filehash or filehash == "":
                debug( "deleting file %s" % fullPath)
                try:
                    os.remove(fullPath)
                except OSError:
                    system( "cmd /C \"attrib -R %s\"" % fullPath )
                    os.remove(fullPath)
            else:
                if forced:
                    warning( "file %s has different hash: %s %s, deleting anyway" % \
                            (fullPath, currentHash, filehash ) )
                try:
                    os.remove(fullPath)
                except OSError:
                    system( "cmd /C \"attrib -R %s\"" % fullPath )
                    os.remove(fullPath)
                else:
                    warning( "file %s has different hash: %s %s, run with option --force to delete it anyway" % \
                            (fullPath, currentHash, filehash ) )
        elif not os.path.isdir(fullPath):
            warning( "file %s does not exist" % fullPath)


def mergeImageDirToRootDir( imagedir, rootdir , linkOnly = varAsBool( emergeSettings.get("General", "UseHardlinks", "False" ))):
    copyDir( imagedir, rootdir , linkOnly)

def moveEntries( srcdir, destdir ):
    for entry in os.listdir( srcdir ):
        #print "rootdir:", root
        debug( "entry: %s" % entry, 1 )
        src = os.path.join( srcdir, entry )
        dest = os.path.join( destdir, entry )
        debug( "src: %s dest: %s" %( src, dest ), 1 )
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
    debug( "fixImageDir: %s %s" % ( imagedir, rootdir ), 1 )
    # imagedir = e:\foo\thirdroot\tmp\dbus-0\image
    # rootdir  = e:\foo\thirdroot
    # files are installed to
    # e:\foo\thirdroot\tmp\dbus-0\image\foo\thirdroot
    _, rootpath = os.path.splitdrive( rootdir )
    #print "rp:", rootpath
    if ( rootpath.startswith( "\\" ) ):
        rootpath = rootpath[1:]
    # CMAKE_INSTALL_PREFIX = X:\
    # -> files are installed to
    # x:\build\foo\dbus\image\
    # --> all fine in this case
    #print "rp:", rootpath
    if len(rootpath) == 0:
        return
    tmp = os.path.join( imagedir, rootpath )
    debug( "tmp: %s" % tmp, 1 )
    tmpdir = os.path.join( imagedir, "tMpDiR" )

    if ( not os.path.isdir( tmpdir ) ):
        os.mkdir( tmpdir )

    moveEntries( tmp, tmpdir )
    os.chdir( imagedir )
    os.removedirs( rootpath )
    moveEntries( tmpdir, imagedir )
    cleanDirectory( tmpdir )
    os.rmdir( tmpdir )

def cleanDirectory( directory ):
    debug("clean directory %s" % directory, 1)
    if ( os.path.exists( directory ) ):
        for root, dirs, files in os.walk( directory, topdown=False):
            for name in files:
                try:
                    os.remove( os.path.join(root, name) )
                except OSError:
                    system( "cmd /C \"attrib -R %s\"" % os.path.join(root, name) )
                    try:
                        os.remove( os.path.join(root, name) )
                    except OSError:
                        die( "couldn't delete file %s\n ( %s )" % ( name, os.path.join( root, name ) ) )
            for name in dirs:
                try:
                    os.rmdir( os.path.join(root, name) )
                except OSError:
                    system( "cmd /C \"attrib -R %s\"" % os.path.join(root, name) )
                    try:
                        os.rmdir( os.path.join(root, name) )
                    except OSError:
                        die( "couldn't delete directory %s\n( %s )" % ( name, os.path.join( root, name ) ) )
    else:
        os.makedirs( directory )

def sedFile( directory, fileName, sedcommand ):
    """ runs the given sed command on the given file """
    olddir = os.getcwd()
    try:
        os.chdir( directory )
        backup = "%s.orig" % fileName
        if( os.path.isfile( backup ) ):
            os.remove( backup )

        command = "sed -i.orig %s %s" % ( sedcommand, fileName )

        system( command )
    finally:
        os.chdir( olddir )

def digestFile( filepath ):
    """ md5-digests a file """
    fileHash = hashlib.md5()
    try:
        with open( filepath, "rb" ) as digFile:
            for line in digFile:
                fileHash.update( line )
            return fileHash.hexdigest()
    except IOError:
        return ""
        

def digestFileSha1( filepath ):
    """ sha1-digests a file """
    fileHash = hashlib.sha1()
    with open( filepath, "rb" ) as hashFile:
        for line in hashFile:
            fileHash.update( line )
    return fileHash.hexdigest()

def getVCSType( url ):
    """ return the type of the vcs url """
    if not url:
        return ""
    if isGitUrl( url ):
        return "git"
    elif url.find("://") == -1:
        return "svn"
    elif url.startswith("[hg]"):
        return "hg"
    elif url.find("svn:") >= 0 or url.find("https:") >= 0 or url.find("http:") >= 0:
        return "svn"
    ## \todo complete more cvs access schemes
    elif url.find("pserver:") >= 0:
        return "cvs"
    else:
        return ""

def isGitUrl( Url ):
    """ this function returns true, if the Url given as parameter is a git url:
        it either starts with git:// or the first part before the first '|' ends with .git
        or if the url starts with the token [git] """
    if Url.startswith('git://'):
        return True
    # split away branch and tags
    splitUrl = Url.split('|')
    if splitUrl[0].endswith(".git"):
        return True
    if Url.startswith("[git]"):
        return True
    return False

def splitVCSUrl( Url ):
    """ this function splits up an url provided by Url into the server name, the path, a branch or tag;
        it will return a list with 3 strings according to the following scheme:
        git://servername/path.git|4.5branch|v4.5.1 will result in ['git://servername:path.git', '4.5branch', 'v4.5.1']
        This also works for all other dvcs"""
    splitUrl = Url.split('|')
    if len(splitUrl) < 3:
        c = [x for x in splitUrl]
        for dummy in range(3 - len(splitUrl)):
            c.append('')
    else:
        c = splitUrl[0:3]
    return c

def replaceVCSUrl( Url ):
    """ this function should be used to replace the url of a server
        this comes in useful if you e.g. need to switch the server url for a push url on gitorious.org """
    configfile = os.path.join(etcPortageDir(), "..", "emergehosts.conf" )
    replacedict = dict()

    # FIXME handle svn/git usernames and settings with a distinct naming
    #todo WTF
    if ( ("General", "KDESVNUSERNAME") in emergeSettings and
     emergeSettings.get("General", "KDESVNUSERNAME") != "username" ) :
        replacedict[ "git://git.kde.org/" ] = "git@git.kde.org:"
    if os.path.exists( configfile ):
        config = configparser.ConfigParser()
        config.read( configfile )
        # add the default KDE stuff if the KDE username is set.
        for section in config.sections():
            host = config.get( section, "host" )
            replace = config.get( section, "replace" )
            replacedict[ host ] = replace

    for host in list(replacedict.keys()):
        if not Url.find( host ) == -1:
            Url = Url.replace( host, replacedict[ host ] )
            break
    return Url

def createImportLibs( dll_name, basepath ):
    """creating the import libraries for the other compiler(if ANSI-C libs)"""

    dst = os.path.join( basepath, "lib" )
    if( not os.path.exists( dst ) ):
        os.mkdir( dst )

    # check whether the required binary tools exist
    HAVE_GENDEF = test4application( "gendef" )
    USE_GENDEF = HAVE_GENDEF
    HAVE_LIB = test4application( "lib" )
    HAVE_DLLTOOL = test4application( "dlltool" )
    if verbose() > 1:
        print("gendef found:", HAVE_GENDEF)
        print("gendef used:", USE_GENDEF)
        print("lib found:", HAVE_LIB)
        print("dlltool found:", HAVE_DLLTOOL)

    dllpath = os.path.join( basepath, "bin", "%s.dll" % dll_name )
    defpath = os.path.join( basepath, "lib", "%s.def" % dll_name )
    exppath = os.path.join( basepath, "lib", "%s.exp" % dll_name )
    imppath = os.path.join( basepath, "lib", "%s.lib" % dll_name )
    gccpath = os.path.join( basepath, "lib", "%s.dll.a" % dll_name )

    if not HAVE_GENDEF and os.path.exists( defpath ):
        HAVE_GENDEF = True
        USE_GENDEF = False
    if not HAVE_GENDEF:
        warning( "system does not have gendef.exe" )
        return False
    if not HAVE_LIB  and not os.path.isfile( imppath ):
        warning( "system does not have lib.exe (from msvc)" )
    if not HAVE_DLLTOOL and not os.path.isfile( gccpath ):
        warning( "system does not have dlltool.exe" )

    # create .def
    if USE_GENDEF:
        cmd = "gendef - %s -a > %s " % ( dllpath, defpath )
        system( cmd )

    if( HAVE_LIB and not os.path.isfile( imppath ) ):
        # create .lib
        cmd = "lib /machine:x86 /def:%s /out:%s" % ( defpath, imppath )
        system( cmd )

    if( HAVE_DLLTOOL and not os.path.isfile( gccpath ) ):
        # create .dll.a
        cmd = "dlltool -d %s -l %s -k" % ( defpath, gccpath )
        system( cmd )

    if os.path.exists( defpath ):
        os.remove( defpath )
    if os.path.exists( exppath ):
        os.remove( exppath )
    return True

def toMSysPath( path ):
    path = path.replace( '\\', '/' )
    if ( len(path) > 1 and path[1] == ':' ):
        path = '/' + path[0].lower() + '/' + path[3:]
    return path

def cleanPackageName( basename, packagename ):
    return os.path.basename( basename ).replace( packagename + "-", "" ).replace( ".py", "" )

def renameDir(src, dest):
    """ rename a directory """
    debug("rename directory from %s to %s" % ( src, dest ), 2)
    if os.rename( src, dest ) == 0:
        return False
    else:
        return True

def createDir(path):
    """Recursive directory creation function. Makes all intermediate-level directories needed to contain the leaf directory"""
    if not os.path.exists( path ):
        debug("creating directory %s " % ( path ), 2)
        os.makedirs( path )
    return True
    
def copyFile(src, dest,linkOnly = varAsBool( emergeSettings.get("General", "UseHardlinks", "False"))):
    """ copy file from src to dest"""
    debug("copy file from %s to %s" % ( src, dest ), 2)
    destDir = os.path.dirname( dest )
    if not os.path.exists( destDir ):
        os.makedirs( destDir )
    if os.path.exists( dest ):
        warning( "Overriding %s" % dest )
        os.remove( dest )
    if linkOnly:
            os.link( src , dest )
    else:
        try:
            shutil.copy(src,dest)
        except OSError:
            system("cmd /C \"attrib -R %s\"" % dest)
            shutil.copy(src,dest)
    return True
    
def copyDir( srcdir, destdir,linkOnly=False ):
    """ copy directory from srcdir to destdir """
    debug( "copyDir called. srcdir: %s, destdir: %s" % ( srcdir, destdir ), 2)

    if ( not srcdir.endswith( "\\" ) ):
        srcdir += "\\"
    if ( not destdir.endswith( "\\" ) ):
        destdir += "\\"

    for root, _, files in os.walk( srcdir ):
        # do not copy files under .svn directories, because they are write-protected
        # and the they cannot easily be deleted...
        if ( root.find( ".svn" ) == -1 ):
            tmpdir = root.replace( srcdir, destdir )
            if not os.path.exists( tmpdir ):
                os.makedirs( tmpdir )
            for fileName in files:
                copyFile(os.path.join( root, fileName ),os.path.join( tmpdir, fileName ))
                debug( "copy %s to %s" % ( os.path.join( root, fileName ), os.path.join( tmpdir, fileName ) ), 2)


def moveDir( srcdir, destdir ):
    """ move directory from srcdir to destdir """
    debug( "moveDir called. srcdir: %s, destdir: %s" % ( srcdir, destdir ), 1 )
    shutil.move( srcdir, destdir )

def rmtree( directory ):
    """ recursively delete directory """
    debug( "rmtree called. directory: %s" % ( directory ), 2 )
    shutil.rmtree ( directory, True ) # ignore errors

def moveFile(src, dest):
    """move file from src to dest"""
    debug("move file from %s to %s" % ( src, dest ), 2)
    os.rename( src, dest )
    return True

def deleteFile(fileName):
    """delete file """
    if not os.path.exists( fileName ):
        return False
    debug("delete file %s " % ( fileName ), 2)
    os.remove( fileName )
    return True

def findFiles( directory, pattern=None, fileNames=None):
    """find files recursivly"""
    if fileNames == None:
        fileNames = []
        pattern = pattern.lower()
    for entry in os.listdir(directory):
        if entry.find(".svn") > -1 or entry.find(".bak") > -1:
            continue
        fileName = os.path.join(directory, entry)
        if os.path.isdir(fileName):
            findFiles(fileName, pattern, fileNames)
        elif os.path.isfile(fileName) and pattern == None or entry.lower().find(pattern) > -1:
            fileNames.append(fileName)
    return fileNames

def putenv(name, value):
    """set environment variable"""
    debug("set environment variable -- set %s=%s" % ( name, value ), 2)
    os.putenv( name, value )
    return True

def unixToDos(filename):
    with open(filename, "rb") as f:
        return str(f.read(),'UTF-8').replace('\n', '\r\n')

def applyPatch(sourceDir, f, patchLevel='0'):
    """apply single patch"""
    cmd = 'patch -d "%s" -p%s < "%s"' % (sourceDir, patchLevel, f)
    debug("applying %s" % cmd)
    if not isCrEol(f):
        p = subprocess.Popen([
            "patch", "-d", sourceDir, "-p", str(patchLevel)],
            stdin = subprocess.PIPE)
        p.communicate(bytes(unixToDos(f),'UTF-8'))
        result = p.wait() == 0
    else:
        result = system( cmd )
    if not result:
        warning( "applying %s failed!" % f)
    return result

def log(fn):
    def inner(*args, **argv):
        logdir = emergeSettings.args.log_dir

        if not logdir:
            return fn(*args, **argv)

        if os.path.isfile(logdir):
            die("EMERGE_LOG_DIR %s is a file" % logdir)

        if not os.path.exists(logdir):
            try:
                os.mkdir(logdir)
            except OSError:
                die("EMERGE_LOG_DIR %s can not be created" % logdir)

        logfile = "%s-%s-%s.log" % (args[0], args[1], args[2])

        logfile = os.path.join(logdir, logfile)
        f = open(logfile, "a+")
        try:
            old_out = sys.stdout
            old_err = sys.stderr
            sys.stdout = f
            sys.stderr = f
            return fn(*args, **argv)
        finally:
            sys.stdout = old_out
            sys.stderr = old_err
            f.close()

    return inner

def getWinVer():
    '''
        Returns the Windows Version of the system returns "0" if the Version
        can not be determined
    '''
    try:
        result = str(subprocess.Popen("cmd /C ver", stdout=subprocess.PIPE).communicate()[0],"windows-1252")
    except OSError:
        debug("Windows Version can not be determined", 1)
        return "0"
    version = re.search(r"\d+\.\d+\.\d+", result)
    if(version):
        return version.group(0)
    debug("Windows Version can not be determined", 1)
    return "0"

def regQuery(key, value):
    '''
    Query the registry key <key> for value <value> and return
    the result.
    '''
    query = 'reg query "%s" /v "%s"' % (key, value)
    debug("Executing registry query %s " % query, 2)
    result = subprocess.Popen(query,
                stdout = subprocess.PIPE).communicate()[0]
    # Output of this command is either an error to stderr
    # or the key with the value in the next line
    reValue = re.compile(r"(\s*%s\s*REG_\w+\s*)(.*)" % value)
    match = reValue.search(str(result, 'windows-1252'))
    if match and match.group(2):
        return match.group(2).rstrip()
    return False

def embedManifest(executable, manifest):
    '''
       Embed a manifest to an executable using either the free
       kdewin manifest if it exists in dev-utils/bin
       or the one provided by the Microsoft Platform SDK if it
       is installed'
    '''
    if not os.path.isfile(executable) or not os.path.isfile(manifest):
        # We die here because this is a problem with the portage files
        die("embedManifest %s or %s do not exist" % (executable, manifest))
    debug("embedding ressource manifest %s into %s" % \
            (manifest, executable), 2)
    mtExe = None
    mtExe = os.path.join(emergeRoot(), "dev-utils", "bin", "mt.exe")

    if(not os.path.isfile(mtExe)):
        # If there is no free manifest tool installed on the system
        # try to fallback on the manifest tool provided by visual studio
        sdkdir = regQuery("HKLM\SOFTWARE\Microsoft\Microsoft SDKs\Windows",
            "CurrentInstallFolder")
        if not sdkdir:
            debug("embedManifest could not find the Registry Key"
                  " for the Windows SDK", 2)
        else:
            mtExe = r'%s' % os.path.join(sdkdir, "Bin", "mt.exe")
            if not os.path.isfile(os.path.normpath(mtExe)):
                debug("embedManifest could not find a mt.exe in\n\t %s" % \
                    os.path.dirname(mtExe), 2)
    if os.path.isfile(mtExe):
        return system([mtExe, "-nologo", "-manifest", manifest,
            "-outputresource:%s;1" % executable])
    else:
        return system(["mt", "-nologo", "-manifest", manifest,
            "-outputresource:%s;1" % executable])


def getscriptname():
    if __name__ == '__main__':
        return sys.argv[ 0 ]
    else:
        return __name__

def prependPath(*parts):
    """put path in front of the PATH environment variable, if it is not there yet.
    The last part must be a non empty string, otherwise we do nothing"""
    if parts[-1]:
        fullPath = os.path.join(*parts)
        old = os.getenv("PATH").split(';')
        if old[0] != fullPath:
            debug("adding %s to system path" % fullPath, 2)
            old.insert(0, fullPath)
            os.putenv( "PATH", ";".join(old))

def setTitle(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)
    
_TIMERS = dict()    
def startTimer(name, level = 0):
    """starts a timer for meassurement"""
    if varAsBool(emergeSettings.get( "EmergeDebug", "MeasureTime", "False")):
        if name in _TIMERS:
            die("%s already in timers" % name)
        _TIMERS[name] = (datetime.datetime.now() , level)
        #if verbose() > 0 and ( level == 0 or verbose() > level):
            #debug( "Task: %s started" % name )
            #sys.stdout.flush()
    
def stopTimer(name):
    """stops a timer for meassurement"""
    if varAsBool(emergeSettings.get( "EmergeDebug", "MeasureTime", "False")):
        if not name in _TIMERS:
            debug( "%s not in timers" % name )
            return
        startTime , level = _TIMERS[name]
        if verbose() > 0  and (level == 0 or verbose() > level):
            print("verbose %s %s" % (verbose(),verbose() > 0))
            delta = datetime.datetime.now() - startTime
            print( "Task: %s stopped after: %s" % (name , delta) )
            sys.stdout.flush()
        del _TIMERS[name]
    

def stopAllTimer():
    """stops all timer for meassurement"""
    keys = sorted(list(_TIMERS.items()) , key=itemgetter(1) , reverse=True)
    for key , _ in keys:
        stopTimer(key)

_SUBST = None
def deSubstPath(path):
    """desubstitude emerge short path"""
    if not varAsBool(emergeSettings.get("General", "EMERGE_USE_SHORT_PATH")):
        return path
    global _SUBST # pylint: disable=W0603
    drive , tail = os.path.splitdrive(path)
    drive = drive.upper()
    if _SUBST == None:
        tmp = str(subprocess.Popen("subst", stdout=subprocess.PIPE).communicate()[0],"windows-1252").split("\r\n")
        _SUBST = dict()
        for s in tmp:
            if s != "":
                key , val = s.split("\\: => ")
                _SUBST[key] = val
    if drive in list(_SUBST.keys()):
        deSubst = _SUBST[drive] + tail
        debug("desubstituded %s to %s" % (path , deSubst) , 1)
        return deSubst
    return path

def notify(title,message,alertClass = None):
    backends = emergeSettings.get( "General","EMERGE_USE_NOTIFY", None)
    if not backends:
        return
    backends = Notifier.NotificationLoader.load(backends.split(";"))
    for backend in backends.values():
        backend.notify(title,message,alertClass)

    

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if not s1:
        return len(s2)
 
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]


#taken from https://bitbucket.org/pypa/setuptools/src/a3d16c5f7443ec6e5e4d8d4791682b56130b41b5/pkg_resources.py?at=default


def parse_version(s):
    """Convert a version string to a chronologically-sortable key

    This is a rough cross between distutils' StrictVersion and LooseVersion;
    if you give it versions that would work with StrictVersion, then it behaves
    the same; otherwise it acts like a slightly-smarter LooseVersion. It is
    *possible* to create pathological version coding schemes that will fool
    this parser, but they should be very rare in practice.

    The returned value will be a tuple of strings.  Numeric portions of the
    version are padded to 8 digits so they will compare numerically, but
    without relying on how numbers compare relative to strings.  Dots are
    dropped, but dashes are retained.  Trailing zeros between alpha segments
    or dashes are suppressed, so that e.g. "2.4.0" is considered the same as
    "2.4". Alphanumeric parts are lower-cased.

    The algorithm assumes that strings like "-" and any alpha string that
    alphabetically follows "final"  represents a "patch level".  So, "2.4-1"
    is assumed to be a branch or patch of "2.4", and therefore "2.4.1" is
    considered newer than "2.4-1", which in turn is newer than "2.4".

    Strings like "a", "b", "c", "alpha", "beta", "candidate" and so on (that
    come before "final" alphabetically) are assumed to be pre-release versions,
    so that the version "2.4" is considered newer than "2.4a1".

    Finally, to handle miscellaneous cases, the strings "pre", "preview", and
    "rc" are treated as if they were "c", i.e. as though they were release
    candidates, and therefore are not as new as a version string that does not
    contain them, and "dev" is replaced with an '@' so that it sorts lower than
    than any other pre-release tag.
    """

    def _parse_version_parts(s):
        component_re = re.compile(r'(\d+ | [a-z]+ | \.| -)', re.VERBOSE)
        replace = {'pre':'c', 'preview':'c','-':'final-','rc':'c','dev':'@'}.get
        for part in component_re.split(s):
            part = replace(part,part)
            if not part or part=='.':
                continue
            if part[:1] in '0123456789':
                yield part.zfill(8)    # pad for numeric comparison
            else:
                yield '*'+part

        yield '*final'  # ensure that alpha/beta/candidate are before final

    parts = []
    for part in _parse_version_parts(s.lower()):
        if part.startswith('*'):
            if part<'*final':   # remove '-' before a prerelease tag
                while parts and parts[-1]=='*final-': parts.pop()
            # remove trailing zeros from each series of numeric parts
            while parts and parts[-1]=='00000000':
                parts.pop()
        parts.append(part)
    return tuple(parts)