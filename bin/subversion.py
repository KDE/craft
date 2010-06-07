# python svn wrapper class
# maybe later we can use the buildin classes
import os
import tools
import re
import sys
import ConfigParser

class Repo_info:
    def __init__( self ):
        """"""
        self.server = None
        self.svnbase = None
        self.svnpath = None
        self.repodir = None
        self.user = None
        self.password = None
        
    def set_repo( self, server, svnbase, repodir, svnpath=None, user=None, password=None ):
        self.server = server
        self.svnbase = svnbase
        self.repodir = repodir
        self.svnpath = svnpath
        self.user = user
        self.password = password
        return self
        
    def readFromURL( self, URL ):
        """ read from any url into the """
        print "readFromURL:", URL
        pattern = "((?:svn\+ssh|svn|:https):\/\/[^/]*)/"
        print "substring: ", re.split( pattern, URL )
        regex = re.compile( pattern )
        print "substring:", regex.sub("", URL )
        
    def __lshift__( self, other ):
        """ self << other """
        self.server = other.server
        self.svnbase = other.svnbase
        self.svnpath = other.svnpath
        self.repodir = other.repodir
        self.user = other.user
        self.password = other.password
        
kde_repo_info = Repo_info().set_repo( user=os.getenv( "KDESVNUSERNAME" ), 
                                      password=os.getenv( "KDESVNPASSWORD" ),
                                      server=os.getenv( "KDESVNSERVER" ),
                                      svnbase="/home/kde/",
                                      repodir=os.getenv( "KDESVNDIR" ) )

class ServerConfig ( tools.Object ):
    def __init__( self ):
        """ ctor """
        """ check if the config file is already in the location """
        # set the path for the config file
        self.configFilePath = os.path.join( os.getenv( "KDEROOT" ), "etc", "svnservers.conf" )
        
        self.config = ConfigParser.ConfigParser()
        
        if not os.path.exists( self.configFilePath ):
            self.inform( "couldn't find subversion server config file:" )
            self.inform( self.configFilePath )
            self.inform( "- adding new one." )
            self.config.set( "DEFAULT", "protocol", "svn" )
            self.config.set( "DEFAULT", "address", "anonsvn.kde.org" )
            self.config.set( "DEFAULT", "base", "/home/kde/" )
            self.config.set( "DEFAULT", "username", "" )
            self.config.set( "DEFAULT", "password", "" )
            try:
                self.config.write( open( self.configFilePath, 'wb' ) )
            except:
                self.error( "couldn't write subversion server config file: %s" % self.configFilePath )
        try:
            self.config.read( os.path.join( self.configFilePath ) )
            sections = self.config.sections()
        except:
            self.die( "couldn't read subversion server config file: %s" % self.configFilePath )
        finally:
            self.inform( "reading subversion server configuration" )
        self.servers = dict()
        for entry in sections:
            self.servers[ entry ] = Repo_info()
            try:
                if self.config.has_option( entry, "username" ):
                    username = self.config.get( entry, "username" )
                if self.config.has_option( entry, "password" ):
                    password = self.config.get( entry, "password" )
                address = self.config.get( entry, "address" )
                protocol = self.config.get( entry, "protocol" )
                base = self.config.get( entry, "base" )
                self.debug("%s %s %s" % ( username, password, '<' + protocol + '://' + address + base + '>' ), 0 )
            except:
                self.error( "reading configuration for server %s epically failed" % entry )

globalServerConfig = ServerConfig()

class Repository ( tools.Object ):
    def __init__( self, repo_info=kde_repo_info, svnpath=None ):
        """ ctor """
        tools.Object.__init__( self )
        self.rinfo = repo_info
        self.rinfo.svnpath = svnpath
        
    def __atomicCheckout( self, recursive=False ):
        """ checkout for one directory """
        repoURL = self.rinfo.server + self.rinfo.svnbase + self.currentsvnpath
        if recursive:
            recursiveOption = ""
        else:
            recursiveOption = "-N "

        command = "svn checkout %s%s" % (recursiveOption, repoURL)
        if ( self.rinfo.user != None ):
            command = command + " --username " + self.rinfo.user
        if ( self.rinfo.password != None ):
            command = command + " --password " + self.rinfo.password
        log = os.tmpfile()
        ret = self.system( command, capture_output=log )
        log.seek( 0 )
        if self.verbose() > 1:
            for line in log:
                print line,
        if ( ret == 0 ):
            return True
        else:
            return False
            
    def __atomicUpdate( self, target, recursive=False ):
        """ update for one directory """
        repoURL = self.rinfo.server + self.rinfo.svnbase + self.currentsvnpath
        if recursive:
            recursiveOption = ""
        else:
            recursiveOption = "-N "        
        
        command = "svn %s update %s" % ( recursiveOption, target )
        if ( self.rinfo.user != None ):
            command = command + " --username " + self.rinfo.user
        if ( self.rinfo.password != None ):
            command = command + " --password " + self.rinfo.password
        log = os.tmpfile()
        ret = self.system( command, capture_output=log )
        log.seek( 0 )
        if self.verbose() > 0:
            for line in log:
                print line,
        if ( ret == 0 ):
            return True
        else:
            return False

    def checkout( self ):
        """ checkout from repository """
        if ( not os.path.exists( self.rinfo.repodir ) ):
            os.makedirs( self.rinfo.repodir )
        else:
            self.warning( "svn checkout destination already exists" )
        
        currentdir = self.rinfo.repodir
        self.currentsvnpath = ""
        os.chdir( self.rinfo.repodir )
        
        for tmpdir in self.rinfo.svnpath.split( '/' )[:-1]:
            currentdir = os.path.join( currentdir, tmpdir )
            self.currentsvnpath += tmpdir
            if not self.__atomicCheckout():
                return False
            self.currentsvnpath += '/'
            os.chdir( currentdir )
        self.currentsvnpath = self.rinfo.svnpath
        if not self.__atomicCheckout( True ):
            return False
        return True
    
    def update( self ):
        """ update local copy """
        if ( not self.localCopyExists() ):
            self.error( "svn update destination directory not existing." )
            return False
        os.chdir( self.rinfo.repodir )
        
        currentdir = self.rinfo.repodir
        self.currentsvnpath = ""
        os.chdir( self.rinfo.repodir )
        
        for target in self.rinfo.svnpath.split( '/' )[ :-1 ]:
            if self.verbose() > 2:
                print "target: ", target
            currentdir = os.path.join( currentdir, target )
            self.currentsvnpath += target
            if not self.__atomicUpdate( target ):
                self.error( 'failed on target: %s' % target )
                return False
            self.currentsvnpath += '/'
            os.chdir( currentdir )
        self.currentsvnpath = os.path.join( self.rinfo.repodir, self.rinfo.svnpath.replace( '/', os.path.sep ) )
        if self.verbose() > 2:
            print "target: ", self.rinfo.svnpath.split( '/' )[ -1 ]
        if not self.__atomicUpdate( self.rinfo.svnpath.split( '/' )[ -1 ], recursive=True ):
            return False
        return True
        
    def status( self ):
        """ check for status """
        """ it will return False if the repository is somehow locked """
        
        target = self.rinfo.svnpath.split( '/' )[ -1 ]
        if ( self.localCopyExists() ):
            # this rather strange line removes the target (the last part of the svnpath) from the svnpath, translates it to a normal path and appends it to the repodir
            os.chdir( os.path.join( self.rinfo.repodir, self.rinfo.svnpath[:-(len(target) + 1)].replace('/', os.path.sep ) ) )
            if not self.isSvnRepo():
                self.warning( "svn destination directory %s is no valid svn directory" % ( self.rinfo.repodir ) )
                return False
                
            command = "svn status %s" % target
            statuslog = os.tmpfile()
            self.system( command, capture_output=statuslog )
            statuslog.seek( 0 )
            
            for line in statuslog:
                if re.match( "^..L.+", line ) or re.match( "^...K.+", line ):
                    self.warning("working copy is locked, needs to be cleaned with cleanup")
                    return False
                if self.verbose() > 1:
                    print line,
            return True
        else:
            self.warning( "svn destination directory not existing." )
            return False
    
    def isSvnRepo( self ):
        if ".svn" not in os.listdir( os.path.join( self.rinfo.repodir, self.rinfo.svnpath.replace('/', os.path.sep ) ) ):
            return False
        else:
            return True
            
    def localCopyExists( self ):
        if ( not os.path.exists( os.path.join( self.rinfo.repodir, self.rinfo.svnpath.replace('/', os.path.sep ) ) ) ):
            return False
        else:
            return True
    
    def cleanup( self ):
        """ eventually cleanup the local copy """
        target = self.rinfo.svnpath.split( '/' )[ -1 ]
        if ( self.localCopyExists() ):
            os.chdir( os.path.join( self.rinfo.repodir, self.rinfo.svnpath.replace('/' + target, '').replace('/', os.path.sep ) ) )
            
            if not self.isSvnRepo():
                self.warning( "svn destination directory is no valid svn directory" )
                return False
                
            command = "svn cleanup %s" % target
            log = os.tmpfile()
            ret = self.system( command, capture_output=log )
            log.seek( 0 )
            if self.verbose() > 1:
                for line in log:
                    self.debug( line )
            if ( ret == 0 ):
                return True
            else:
                return False
        else:
            self.warning( "svn destination directory not existing." )
            return False

    def info( self ):
        """ return dictionary of the svn info command """
        """ be aware that this function is running within repodir """
        os.chdir( self.rinfo.repodir )
        self.debug( self.rinfo.repodir )
        log = os.tmpfile()
        self.system( "svn info", capture_output=log )
        log.seek( 0 )
        infos = dict()
        for line in log:
            if self.verbose() > 2:
                self.debug( line )
            if re.match( "^.*: .*\r\n", line ):
                [key, value] = re.split(": ", line, 1 )
                value = value.strip()
                if self.verbose() > 2:
                    self.debug( [key, value] )
                infos[ key ] = value
        self.debug( infos )
        return infos
    
    def runSelfTests( self ):
        """ define some tests to make sure this class works """
        
        self.rinfo.repodir = "D:\\sources\\subversiontest\\trunk\\kdesupport\\emerge"
#        self.rinfo.repodir = "D:\\sources\\subversiontest"
#        self.rinfo.svnpath = "trunk/kdesupport/emerge"
        self.increase( 0, 0, 0, 0 )
#        self.increase( 0, 0, 0, 0 )
        
        self.debug("checkout: ...")
        #self.checkout()
        self.inform("checkout done")
        self.debug("status: ...")
        #self.status()
        self.inform("status done")
        self.debug("cleanup: ...")
        #self.cleanup()
        self.inform("cleanup done")
        self.debug("update: ...")
        #self.update()
        self.inform("update done")
        self.debug("info: ...")
#        infodict = self.info()
#        print Repo_info().readFromURL( infodict['URL'] )
        self.inform("info done")
        
        
if __name__ == '__main__':
    Repository().runSelfTests()
