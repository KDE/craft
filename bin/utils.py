# -*- coding: utf-8 -*-
"""@brief utilities 
this file contains some helper functions for emerge
"""

# copyright:
# Holger Schroeder <holger [AT] holgis [DOT] net>
# Patrick Spendrin <ps_ml [AT] gmx [DOT] de>
# Ralf Habacker <ralf.habacker [AT] freenet [DOT] de>

import httplib
import ftplib
import os.path
import sys
import urlparse
import shutil
import zipfile
import tarfile
import hashlib
import traceback
import tempfile
import getpass
import subprocess
import re
import tempfile

if os.name == 'nt': import msvcrt
else:               import fcntl

import info
import portage

import ConfigParser

import portage_versions


def isSourceOnly():
    return os.getenv("EMERGE_SOURCEONLY") == "True" or os.getenv("EMERGE_SOURCEONLY") == "1"

SVN_LOCK_FILE = "emergesvn-%s.lck"

def svnLockFileName():
    '''Generate a user global svn lock file.
       TODO: generate it smarter to prevent security issues
             and possible collisions.
    '''
    do_lock = os.environ.get("EMERGE_SVN_LOCK")
    if not do_lock or do_lock.strip().lower() not in ("true", "yes"):
        return None

    try:
        return os.environ["EMERGE_SVN_LOCK_FILE"]
    except KeyError:
        pass

    return os.path.join(
        tempfile.gettempdir(), SVN_LOCK_FILE % getpass.getuser())

class LockFile(object):
    """Context manager for a user global lock file"""

    def __init__(self, file_name):
        self.file_name   = file_name
        self.file_handle = None

    def __enter__(self):
        if not self.file_name: return

        self.file_handle = open(self.file_name, 'a')
        fh = self.file_handle

        if os.name == 'nt':
            fh.seek(0)
            while True:
                try:
                    msvcrt.locking(fh.fileno(), msvcrt.LK_LOCK, 2147483647L)
                except IOError, msg:
                    # after 15 secs (every 1 sec, 1 attempt -> 15 secs)
                    # a exception is raised but we want to continue trying.
                    continue
                break
        else:
            fcntl.flock(fh, fcntl.LOCK_EX)

        fh.truncate(0)
        print >> fh, "%d" % os.getpid()
        fh.flush()

    def __exit__(self, exc_type, exc_value, exc_tb):
        fh = self.file_handle
        if fh is None: return
        self.file_handle = None
        if os.name == 'nt':
            fh.seek(0)
            msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 2147483647L)
        else:
            fcntl.flock(fh, fcntl.LOCK_UN)
        try:
            fh.close()
        except:
            traceback.print_exc()

### fetch functions

#FIXME: get this from somewhere else:
WGetExecutable = os.path.join( os.getenv( "KDEROOT" ), "bin", "wget.exe" )
if not os.path.exists( WGetExecutable ):
    WGetExecutable = os.path.join( os.getenv( "KDEROOT" ), "dev-utils", "bin", "wget.exe" )

def test4application( appname, args=None ):
    """check if the application specified by 'appname' is available"""
    try:
        f = file('NUL:')
        p = subprocess.Popen( appname, stdout=f, stderr=f )
        p.wait()
        return True
    except:
        debug( "could not find application %s" % appname, 1 )
        return False

def verbose():
    """return the value if the verbose level""" 
    verb = os.getenv( "EMERGE_VERBOSE" )
    if ( not verb == None and verb.isdigit() and int(verb) > 0 ):
        return int( verb )
    else:
        return 0

def getFiles( urls, destdir, suffix=''):
    """download files from 'url' into 'destdir'"""
    debug( "getfiles called. urls: %s" % urls, 1 )
    # make sure distfiles dir exists
    if ( not os.path.exists( destdir ) ):
        os.makedirs( destdir )

    for url in urls.split():
        if ( not getFile( url + suffix, destdir ) ):
            return False

    return True

def getFile( url, destdir ):
    """download file from 'url' into 'destdir'"""
    debug( "getFile called. url: %s" % url, 1 )
    if url == "":
        error( "fetch: no url given" )
        return False


    wgetpath = WGetExecutable
    if ( os.path.exists( wgetpath ) ):
        return wgetFile( url, destdir )

    scheme, host, path, params, qu, fr = urlparse.urlparse( url )


    filename = os.path.basename( path )
    debug( "%s\n%s\n%s\n%s" % ( scheme, host, path, filename ) )

    if ( scheme == "http" ):
        return getHttpFile( host, path, destdir, filename )
    elif ( scheme == "ftp" ):
        return getFtpFile( host, path, destdir, filename )
    else:
        error( "getFile: protocol not understood" )
        return False

def wgetFile( url, destdir , filename=''):
    """download file with wget from 'url' into 'destdir', if filename is given to the file specified"""
    compath = WGetExecutable
    command = "%s --no-check-certificate -c -t 10" % compath
    if os.environ.get("EMERGE_NO_PASSIVE_FTP"):
        command += " --no-passive-ftp "
    if(filename ==''):
       command += "  -P %s" % destdir
    else:
       command += " -O %s" % os.path.join( destdir , filename )
    command += " %s" % url
    debug( "wgetfile called", 1 )
    ret = system( command )
    debug( "wget ret: %s" % ret, 2)
    return ret

def getFtpFile( host, path, destdir, filename ):
    """download file from a ftp host specified by 'host' and 'path' into 'destdir' using 'filename' as file name"""
    # FIXME check return values here (implement useful error handling)...
    debug( "FIXME getFtpFile called. %s %s" % ( host, path ), 1 )

    outfile = open( os.path.join( destdir, filename ), "wb" )
    ftp = ftplib.FTP( host )
    ftp.login( "anonymous", "johndoe" )
    ftp.retrbinary( "RETR " + path, outfile.write )

    outfile.close()
    return True

def getHttpFile( host, path, destdir, filename ):
    """download file from a http host specified by 'host' and 'path' into 'destdir' using 'filename' as file name"""
    # FIXME check return values here (implement useful error handling)...
    debug( "getHttpFile called. %s %s" % ( host, path ) , 1 )

    conn = httplib.HTTPConnection( host )
    conn.request( "GET", path )
    r1 = conn.getresponse()
    debug( "status: %s; reason: %s" % ( str( r1.status ), str( r1.reason ) ) )
        
    count = 0
    while r1.status == 302:
        if count > 10:
            print "Redirect loop"
            return False
        count += 1
        scheme, host, path, params, qu, fr = urlparse.urlparse( r1.getheader( "Location" ) )
        debug( "Redirection: %s %s" % ( host, path ), 1 )
        conn = httplib.HTTPConnection( host )
        conn.request( "GET", path )
        r1 = conn.getresponse()
        debug( "status: %s; reason: %s" % ( str( r1.status ), str( r1.reason ) ) )
    
        
    data = r1.read()

    f = open( os.path.join( destdir, filename ), "wb" )
    f.write( data )
    f.close()
    return True

def isCrEol(filename):
    with open(filename, "rb") as f:
        return f.readline().endswith("\r\n")

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
        file = os.path.join( downloaddir,filename )
        if digests == None:
            digestFile = file + '.sha1'
            if not os.path.exists( digestFile ):
                digestFile, _ = os.path.splitext( file )
                digestFile += '.sha1'
                if not os.path.exists( digestFile ):
                    error( "digest validation request for file %s, but no digest  file present" %
                            file )
                    return False
            hash = digestFileSha1( file )
            f = open( digestFile , "r" )
            line = f.readline()
            f.close()
            digest = re.search('\\b[0-9a-fA-F]{40}\\b', line)
            if not digest:
                error( " digestFile %s for file %s does not contain a valid checksum" % (digestFile,
                        file,) )
                return False
            digest = digest.group(0)
            if len(digest) != len(hash) or digest.find(hash) == -1:
                error( "digest value for file %s (%s) do not match (%s)" % (file, hash, digest) )
                return False
        # digest provided in digests parameter
        else:
            hash = digestFileSha1( file )
            digest = digestList[i].strip()
            if len(digest) != len(hash) or digest.find(hash) == -1:
                error( "digest value for file %s (%s) do not match (%s)" % (file, hash, digest) )
                return False
        i = i + 1
    return True

    
def createFilesDigests( downloaddir, filenames ):
    """create digests of (multiple) files specified by 'filenames' from 'downloaddir'"""
    digestList = list()
    for filename in filenames:
        file = os.path.join( downloaddir,filename )
        digest = digestFileSha1( file )
        entry = filename, digest
        digestList.append(entry)
    return digestList
    
def printFilesDigests( digestFiles, buildTarget=None):
    size = len( digestFiles )
    i = 0
    for (file,digest) in digestFiles:
        print "%40s %s" % ( file, digest ),
        if size == 1:
            if buildTarget==None:
                print "      '%s'" % ( digest )
            else:
                print "self.targetDigests['%s'] = '%s'" % ( buildTarget,digest )
        else:
            if buildTarget==None:
                if i == 0: 
                    print "      ['%s'," % ( digest )
                elif i == size-1: 
                    print "       '%s']" % ( digest )
                else:
                    print "       '%s'," % ( digest )
                i = i + 1
            else:
                if i == 0: 
                    print "self.targetDigests['%s'] = ['%s'," % ( buildTarget,digest )
                elif i == size-1: 
                    print "                             '%s']" % ( digest )
                else:
                    print "                             '%s'," % ( digest )
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

def un7zip( file, destdir ):
    command = "7za x -r -y -o%s %s" % ( destdir, file )
    if verbose() > 1:
        return system( command )
    else:
        tmp = tempfile.TemporaryFile()
        return system( command, tmp )
	
def unTar( file, destdir ):
    """unpack tar file specified by 'file' into 'destdir'"""
    debug( "unTar called. file: %s, destdir: %s" % ( file, destdir ), 1 )
    ( shortname, ext ) = os.path.splitext( file )
	
    mode = "r"
    if ( ext == ".gz" ):
        mode = "r:gz"
    elif ( ext == ".bz2" ):
        mode = "r:bz2"
    elif( ext == ".lzma" or ext == ".xz" ):
        un7zip( file , os.getenv("TMP") )
        (srcpath , tarname ) = os.path.split( shortname )
        file=os.path.join( os.getenv("TMP") , tarname )

    if not os.path.exists( file ):
        error( "couldn't find file %s" % file )
        return False

    try:
        tar = tarfile.open( file, mode )
    except:
        error( "could not open existing tar archive: %s" % file )
        return False

    # FIXME how to handle errors here ?
    for foo in tar:
        try:
            tar.extract( foo, destdir )
        except:
            error( "couldn't extract file %s to directory %s" % ( foo, destdir ) )
            return False

    return True

def unZip( file, destdir ):
    """unzip file specified by 'file' into 'destdir'"""
    debug( "unZip called: file %s to destination %s" % ( file, destdir ), 1 )

    if not os.path.exists( destdir ):
        os.makedirs( destdir )

    try:
        zip = zipfile.ZipFile( file )
    except:
        error( "couldn't extract file %s" % file )
        return False

    for i, name in enumerate( zip.namelist() ):
        if not name.endswith( '/' ):
            dirname = os.path.join( destdir, os.path.dirname( name ) )

            if not os.path.exists( dirname ):
                os.makedirs( dirname )

            outfile = open( os.path.join( destdir, name ), 'wb' )
            outfile.write( zip.read( name ) )
            outfile.flush()
            outfile.close()

    return True

### svn fetch/unpack functions

def svnFetch( repo, destdir, username = None, password = None ):
    debug( "utils svnfetch: repo %s to destination %s" % ( repo, destdir ), 1 )
    if ( not os.path.exists( destdir ) ):
        os.makedirs( destdir )
    os.chdir( destdir )

    ret = 0
    #if ( len( os.listdir( destdir ) ) == 0 ):

    dir = os.path.basename( repo.replace( "/", "\\" ) )
    path = os.path.join( destdir, dir )
    debug( "path: %s" % path, 1 ) 
    if ( not os.path.exists( path ) ):
        # not checked out yet
        command = "svn checkout %s" % repo
        if ( username != None ):
            command = command + " --username " + username
        if ( password != None ):
            command = command + " --password " + password
        with LockFile(svnLockFileName()):
            ret = system( command )
    else:
        # already checked out, so only update
        mode = "update"
        os.chdir( path )
        debug( "svn up cwd: %s" % os.getcwd(), 1 )
        with LockFile(svnLockFileName()):
            ret = system( "svn update" )

    if ( ret == 0 ):
        return True
    else:
        return False

### package dependencies functions

def checkManifestFile( name, category, package, version ):
    if os.path.isfile( name ):
        f = open( name, "rb" )
        header = f.readline()
        line = f.readline()
        f.close()
        if not '/' in line:
            """ update the file """
            line = "%s/%s:%s:%s" % ( package, category, package, version )
            f = open( name, "wb" )
            f.write( header )
            f.write( line )
        if ( line.startswith( "%s/%s:%s:" % ( category, package, version ) ) ):
            return True
    return False


def info( message ):
    if verbose() > 0:
        print "emerge info: %s" % message
    return True

def debug( message, level=0 ):
    if verbose() > level:
        print "emerge debug:", message
    sys.stdout.flush()
    return True

def warning( message ):
    if verbose() > 0:
        print "emerge warning: %s" % message
    return True

def new_line( level=0 ):
    if verbose() > level:
        print

def debug_line( level=0 ):
    if verbose() > level:
        print "_" * 80

def error( message ):
    if verbose() > 0:
        print >> sys.stderr, "emerge error: %s" % message
    return False

def die( message ):
    print >> sys.stderr, "emerge fatal error: %s" % message
    exit( 1 )

def system( cmd, outstream=None, errstream=None, *args, **kw ):

    if outstream is None: outstream = sys.stdout
    if errstream is None: errstream = sys.stderr

    debug( "executing command: %s" % str(cmd), 1 )
    redirected = False
    try:
        if verbose() == 0 and outstream == sys.stdout and errstream == sys.stderr:
            redirected = True
            sys.stderr = file('test.outlog', 'wb')
            sys.stdout = sys.stderr

        p = subprocess.Popen( cmd, shell=True, stdout=outstream,
                stderr=errstream, *args, **kw )
        ret = p.wait()
    finally:
        if redirected:
            sys.stderr = sys.__stderr__
            sys.stdout = sys.__stdout__

    return ( ret == 0 )

def systemWithoutShell(cmdstring, outstream=sys.stdout, errstream=sys.stderr):
    debug( "executing command: %s" % cmdstring, 1 )
    if verbose() == 0 and outstream == sys.stdout and errstream == sys.stderr:
        sys.stderr = file('test.outlog', 'wb')
        sys.stdout = sys.stderr
    p = subprocess.Popen( cmdstring, stdout=outstream, stderr=errstream )
    ret = p.wait()
    sys.stderr = sys.__stderr__
    sys.stdout = sys.__stdout__
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

    for root, dirs, files in os.walk( imagedir ):
        for file in files:
            ret.append( ( os.path.join( root, file ).replace( myimagedir, "" ), digestFile( os.path.join( root, file ) ) ) )
    return ret
    
def getFileListFromManifest( rootdir, package ):
    """ return file list according to the manifest files for deletion/import """
    fileList = []
    manifestDir = os.path.join( rootdir, "manifest" )
    if os.path.exists( manifestDir ):
        for file in os.listdir( manifestDir ):
            if file.endswith( ".mft" ):
                [ pkg, version ] = portage.packageSplit( file.replace( ".mft", "" ) )
                if file.endswith( ".mft" ) and package==pkg:
                    fptr = open( os.path.join( rootdir, "manifest", file ), 'rb' )
                    for line in fptr:
                        try:
                            line = line.replace( "\n", "" ).replace( "\r", "" )
                            # check for digest having two spaces between filename and hash
                            if not line.find( "  " ) == -1:
                                [ b, a ] = line.rsplit( "  ", 2 )
                            # check for filname have spaces
                            elif line.count( " " ) > 1:
                                ri = line.rindex( " " )
                                b = line[ ri: ]
                                a = line[ : ri - 1 ]
                            # check for digest having one spaces
                            elif not line.find( " " ) == -1:
                                [ a, b ] = line.rsplit( " ", 2 )
                            else:
                                a, b = line, ""
                        except:
                            utils.die( "could not parse line %s" % line, 1 )
                            
                        if os.path.join( rootdir, "manifest", file ) == os.path.join( rootdir, os.path.normcase( a ) ):
                            continue
                        fileList.append( ( a, b ) )
                    fptr.close()
        else:
            debug( "could not find any manifest files", 2 )
    else:
        debug( "could not find manifest directory", 2 )
    return fileList

def unmergeFileList( rootdir, fileList, forced = False ):
    """ delete files in the fileList """
    debug( "unmergeFileList called for %s files" % str( len( fileList ) ), 2 )
    for (filename, filehash) in fileList:
        if os.path.isfile( os.path.join( rootdir, os.path.normcase( filename ) ) ):
            hash = digestFile( os.path.join( rootdir, os.path.normcase( filename ) ) )
            if hash == filehash or filehash == "":
                debug( "deleting file %s" % os.path.join( rootdir, os.path.normcase( filename ) ) )
                os.remove( os.path.join( rootdir, os.path.normcase( filename ) ) )
            else:
                warning( "file %s has different hash: %s %s, run with option --force to delete it anyway" % ( os.path.join( rootdir, os.path.normcase( filename ) ), hash, filehash ) )
                if forced:
                    os.remove( os.path.join( rootdir, os.path.normcase( filename ) ) )
        elif not os.path.isdir( os.path.join( rootdir, os.path.normcase( filename ) ) ):
            warning( "file %s does not exist" % ( os.path.join( rootdir, os.path.normcase( filename ) ) ) )
        
def unmerge( rootdir, package, forced = False ):
    """ delete files according to the manifest files """
    debug( "unmerge called: %s" % ( package ), 2 )
    removed = False
    manifestDir = os.path.join( rootdir, "manifest"  ) 
    if os.path.exists( manifestDir ):
        for file in os.listdir( manifestDir ):
            if file.endswith(".mft"):
                [ pkg, version ] = portage.packageSplit( file.replace( ".mft", "" ) )
                if file.endswith( ".mft" ) and package==pkg:
                    fptr = open( os.path.join( rootdir, "manifest", file ), 'rb' )
                    for line in fptr:
                        try:
                            line = line.replace( "\n", "" ).replace( "\r", "" )
                            # check for digest having two spaces between filename and hash
                            if not line.find( "  " ) == -1:
                                [ b, a ] = line.rsplit( "  ", 2 )
                            # check for filname have spaces
                            elif line.count(" ") > 1:
                                ri = line.rindex(" ")
                                b = line[ri:]
                                a = line[:ri-1]
                            # check for digest having one spaces
                            elif not line.find( " " ) == -1:
                                [ a, b ] = line.rsplit( " ", 2 )
                            else:
                                a, b = line, ""
                        except:
                            utils.die("could not parse line %s" % line,1)
                            
                        if os.path.join( rootdir, "manifest", file ) == os.path.join( rootdir, os.path.normcase( a ) ):
                            continue
                        if os.path.isfile( os.path.join( rootdir, os.path.normcase( a ) ) ):
                            hash = digestFile( os.path.join( rootdir, os.path.normcase( a ) ) )
                            if b == "" or hash == b:
                                debug( "deleting file %s" % a )
                                os.remove( os.path.join( rootdir, os.path.normcase( a ) ) )
                            else:
                                warning( "file %s has different hash: %s %s, run with option --force to delete it anyway" % ( os.path.normcase( a ), hash, b ) )
                                if forced:
                                    os.remove( os.path.join( rootdir, os.path.normcase( a ) ) )
                        elif not os.path.isdir( os.path.join( rootdir, os.path.normcase( a ) ) ):
                            warning( "file %s does not exist" % ( os.path.normcase( a ) ) )
                    fptr.close()
                    os.remove( os.path.join( rootdir, "manifest", file ) )
                    removed = True
                    
        else:
            debug("could not find any manifest files",2)
    else:
        debug("could not find manifest directory",2)
        
    return removed

def manifestDir( srcdir, imagedir, category, package, version ):
    if not hasManifestFile( imagedir, category, package ):
        createManifestFiles( imagedir, imagedir, category, package, version )

def hasManifestFile( imagedir, category, package ):
    if os.path.exists( os.path.join( imagedir, "manifest"  ) ):
        for file in os.listdir( os.path.join( imagedir, "manifest"  ) ):
            if file.startswith( package ) and file.endswith( "-bin.mft" ):
                return True
    return False
    
def createManifestFiles( imagedir, destdir, category, package, version ):
    """create the manifest files for an imagedir like the kdewin-packager does"""
    debug( "createManifestFiles called: %s %s %s %s %s" % ( imagedir, destdir, category, package, version ), 1 )

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
                binList.append( os.path.join( root, file ).replace( myimagedir, "" ) )
            if dirType == 2:
                if file.endswith( ".a" ) or file.endswith( ".lib" ):
                    libList.append( os.path.join( root, file ).replace( myimagedir, "" ) )
                else:
                    binList.append( os.path.join( root, file ).replace( myimagedir, "" ) )
            if dirType == 3 or dirType == 4 or dirType == 5:
                binList.append( os.path.join( root, file ).replace( myimagedir, "" ) )
            if dirType == 6:
                libList.append( os.path.join( root, file ).replace( myimagedir, "" ) )
            if dirType == 7 or dirType == 8:
                docList.append( os.path.join( root, file ).replace( myimagedir, "" ) )

    if not os.path.exists( os.path.join( destdir, "manifest" ) ):
        os.makedirs( os.path.join( destdir, "manifest" ) )

    if len(binList) > 0:
        binmanifest = open( os.path.join( destdir, "manifest", "%s-%s-bin.mft" % ( package, version )), 'wb' )
    if len(libList) > 0:
        libmanifest = open( os.path.join( destdir, "manifest", "%s-%s-lib.mft" % ( package, version )), 'wb' )
    if len(docList) > 0:
        docmanifest = open( os.path.join( destdir, "manifest", "%s-%s-doc.mft" % ( package, version )), 'wb' )
#    if verbose() >= 1:
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
        binversion = open( os.path.join( destdir, "manifest", "%s-%s-bin.ver" % ( package, version )), 'wb' )
    if len(libList) > 0:
        libversion = open( os.path.join( destdir, "manifest", "%s-%s-lib.ver" % ( package, version )), 'wb' )
    if len(docList) > 0:
        docversion = open( os.path.join( destdir, "manifest", "%s-%s-doc.ver" % ( package, version )), 'wb' )
    if len(binList) > 0:
        binversion.write( "%s %s Binaries\n%s/%s:%s:unknown" % ( package, version, category, package, version ) )
    if len(libList) > 0:
        libversion.write( "%s %s developer files\n%s/%s:%s:unknown" % ( package, version, category, package, version ) )
    if len(docList) > 0:
        docversion.write( "%s %s Documentation\n%s/%s:%s:unknown" % ( package, version, category, package, version ) )
    return True

def mergeImageDirToRootDir( imagedir, rootdir ):
    copySrcDirToDestDir( imagedir, rootdir )

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
    ( rootdrive, rootpath ) = os.path.splitdrive( rootdir )
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

def cleanDirectory( dir ):
    debug("clean directory %s" % dir,1)
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
    olddir = os.getcwd()
    try:
        os.chdir( directory )
        backup = "%s.orig" % file
        if( os.path.isfile( backup ) ):
            os.remove( backup )

        command = "sed -i.orig %s %s" % ( sedcommand, file )

        system( command )
    finally:
        os.chdir( olddir )

def digestFile( filepath ):
    """ md5-digests a file """
    hash = hashlib.md5()
    file = open( filepath, "rb" )
    for line in file:
        hash.update( line )
    file.close()
    return hash.hexdigest()

def digestFileSha1( filepath ):
    """ sha1-digests a file """
    hash = hashlib.sha1()
    file = open( filepath, "rb" )
    for line in file:
        hash.update( line )
    file.close()
    return hash.hexdigest()

def getVCSType( url ):
    """ return the type of the vcs url """
    if url.find("://") == -1:
        return "svn"
    elif url.startswith("[hg]"):
        return "hg"
    elif isGitUrl( url ):
        return "git"
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

def splitGitUrl( Url ):
    """ this function splits up an url provided by Url into the server name, the path, a branch or tag; 
        it will return a list with 3 strings according to the following scheme:
        git://servername/path.git|4.5branch|v4.5.1 will result in ['git://servername:path.git', '4.5branch', 'v4.5.1']
        This also works for all other dvcs"""
    splitUrl = Url.split('|')
    if len(splitUrl) < 3:
        c = [x for x in splitUrl]
        for y in range(3 - len(splitUrl)): c.append('')
    else:
        c = splitUrl[0:3]
    return c

def replaceVCSUrl( Url ):
    """ this function should be used to replace the url of a server
        this comes in useful if you e.g. need to switch the server url for a push url on gitorious.org """
    configfile = os.path.join( portage.etcDir(), "..", "emergehosts.conf" )
    replacedict = dict()

    # FIXME handle svn/git usernames and settings with a distinct naming
    if ( os.getenv( "KDESVNUSERNAME" ) and
         os.getenv( "KDESVNUSERNAME" ) != "username" ) :
        replacedict[ "git://git.kde.org/" ] = "git@git.kde.org:"
    if os.path.exists( configfile ):
        config = ConfigParser.ConfigParser()
        config.read( configfile )
        # add the default KDE stuff if the KDE username is set.
        for section in config.sections():
            host = config.get( section, "host" )
            replace = config.get( section, "replace" )
            replacedict[ host ] = replace
            
    for host in replacedict.keys():
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
    HAVE_PEXPORTS = test4application( "pexports" )
    USE_PEXPORTS = HAVE_PEXPORTS
    HAVE_LIB = test4application( "lib" )
    HAVE_DLLTOOL = test4application( "dlltool" )
    if verbose() > 1:
        print "pexports found:", HAVE_PEXPORTS
        print "pexports used:", USE_PEXPORTS
        print "lib found:", HAVE_LIB
        print "dlltool found:", HAVE_DLLTOOL
    
    dllpath = os.path.join( basepath, "bin", "%s.dll" % dll_name )
    defpath = os.path.join( basepath, "lib", "%s.def" % dll_name )
    exppath = os.path.join( basepath, "lib", "%s.exp" % dll_name )
    imppath = os.path.join( basepath, "lib", "%s.lib" % dll_name )
    gccpath = os.path.join( basepath, "lib", "%s.dll.a" % dll_name )

    if not HAVE_PEXPORTS and os.path.exists( defpath ):
        HAVE_PEXPORTS = True
        USE_PEXPORTS = False
    if not HAVE_PEXPORTS:
        warning( "system does not have pexports.exe" )
        return False
    if not HAVE_LIB:
        warning( "system does not have lib.exe (from msvc)" )
        if not HAVE_DLLTOOL:
            warning( "system does not have dlltool.exe" )
            return False

    # create .def
    if USE_PEXPORTS:
        cmd = "pexports %s > %s " % ( dllpath, defpath )
        system( cmd )
        sedcmd = "sed -i \"s/^LIBRARY.*$/LIBRARY %s.dll/\" %s" % (dll_name, defpath)
        system( sedcmd )

    if( HAVE_LIB and not os.path.isfile( imppath ) ):
        # create .lib
        cmd = "lib /machine:x86 /def:%s /out:%s" % ( defpath, imppath )
        system( cmd )

    if( HAVE_DLLTOOL and not os.path.isfile( gccpath ) ):
        # create .dll.a
        cmd = "dlltool -d %s -l %s" % ( defpath, gccpath )
        system( cmd )
        
    if os.path.exists( defpath ):
        os.remove( defpath )
    if os.path.exists( exppath ):
        os.remove( exppath )
    return True

def toMSysPath( path ):
    path = path.replace( '\\', '/' )
    if ( path[1] == ':' ):
      path = '/' + path[0].lower() + '/' + path[3:]
    return path

def cleanPackageName( basename, packagename ):
    return os.path.basename( basename ).replace( packagename + "-", "" ).replace( ".py", "" )
    
def renameDir(src,dest):
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
    
def copyDir( srcdir, destdir ):
    """ copy directory from srcdir to destdir """
    debug( "copyDir called. srcdir: %s, destdir: %s" % ( srcdir, destdir ) , 2)

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
                debug( "copy %s to %s" % ( os.path.join( root, file ), os.path.join( tmpdir, file ) ) , 2) 

def moveDir( srcdir, destdir ):
    """ move directory from srcdir to destdir """
    debug( "moveDir called. srcdir: %s, destdir: %s" % ( srcdir, destdir ), 1 )
    shutil.move( srcdir, destdir )
    
def rmtree( dir ):
    """ recursively delete dir """
    debug( "rmtree called. dir: %s" % ( dir ), 2 )
    shutil.rmtree ( dir, True ) # ignore errors

def copyFile(src,dest):
    """ copy file from src to dest"""
    debug("copy file from %s to %s" % ( src, dest ), 2)
    shutil.copy( src, dest )
    return True

def moveFile(src,dest):
    """move file from src to dest"""
    debug("move file from %s to %s" % ( src, dest ), 2)
    os.rename( src, dest )
    return True
    
def deleteFile(file):
    """delete file """
    if not os.path.exists( file ):
        return False
    debug("delete file %s " % ( file ), 2)
    os.remove( file )
    return True

def findFiles( dir, pattern=None, list=None):
    """find files recursivly""" 
    if list == None: 
        list = []
        pattern = pattern.lower()
    for entry in os.listdir(dir):
        if entry.find(".svn") > -1 or entry.find(".bak") > -1:
            continue
        file = os.path.join(dir, entry)
        if os.path.isdir(file):
            findFiles(file,pattern,list)
        elif os.path.isfile(file) and pattern == None or entry.lower().find(pattern) > -1:
            list.append(file)
    return list
    
def putenv(name, value):
    """set environment variable"""
    debug("set environment variable -- set %s=%s" % ( name, value ), 2)
    os.putenv( name, value )
    return True

def unixToDos(filename):
    with open(filename, "rb") as f:
        return f.read().replace('\n', '\r\n')

def applyPatch(sourceDir, f, patchLevel='0'):
    """apply single patch"""
    cmd = "patch -d %s -p%s < %s" % (sourceDir, patchLevel, f)
    debug("applying patch %s" % cmd, 2)
    if not isCrEol(f):
        p = subprocess.Popen([
            "patch", "-d", sourceDir, "-p", str(patchLevel)],
            stdin=subprocess.PIPE)
        p.communicate(unixToDos(f))
        return p.wait() == 0
    else:
        return system( cmd )

def log(fn):
    def inner(*args, **argv):

        logdir = os.environ.get('EMERGE_LOG_DIR')

        if not logdir:
            return fn(*args, **argv)

        if os.path.isfile(logdir):
            die("EMERGE_LOG_DIR %s is a file" % logdir)

        if not os.path.exists(logdir):
            try:
                os.mkdir(logdir)
            except:
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

def getscriptname():
    if __name__ == '__main__':
        return sys.argv[ 0 ]
    else:
        return __name__
