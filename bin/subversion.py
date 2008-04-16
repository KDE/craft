# python svn wrapper class
# maybe later we can use the buildin classes
import os
import tools
import re
import sys

class repo_info:
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
        
    def __lshift__( self, other ):
        """ self << other """
        self.server = other.server
        self.svnbase = other.svnbase
        self.svnpath = other.svnpath
        self.repodir = other.repodir
        self.user = other.user
        self.password = other.password
        
kde_repo_info = repo_info().set_repo( user=os.getenv( "KDESVNUSERNAME" ), 
                                      password=os.getenv( "KDESVNPASSWORD" ),
                                      server=os.getenv( "KDESVNSERVER" ),
                                      svnbase="/home/kde/",
                                      repodir=os.getenv( "KDESVNDIR" ) )


class repository ( tools.emerge_container ):
    def __init__( self, info=kde_repo_info, svnpath=None ):
        """ ctor """
        self.info = info
        self.info.svnpath = svnpath
        self.verb = "1"

    def __atomicCheckout( self, recursive=False ):
        """ checkout for one directory """
        repoURL = self.info.server + self.info.svnbase + self.currentsvnpath
        if recursive:
            recursiveOption = ""
        else:
            recursiveOption = "-N "

        command = "svn checkout %s%s" % (recursiveOption, repoURL)
        if ( self.info.user != None ):
            command = command + " --username " + self.info.user
        if ( self.info.password != None ):
            command = command + " --password " + self.info.password
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
        repoURL = self.info.server + self.info.svnbase + self.currentsvnpath
        if recursive:
            recursiveOption = ""
        else:
            recursiveOption = "-N "        
        
        command = "svn %s update %s" % ( recursiveOption, target )
        if ( self.info.user != None ):
            command = command + " --username " + self.info.user
        if ( self.info.password != None ):
            command = command + " --password " + self.info.password
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

    def checkout( self ):
        """ checkout from repository """
        if ( not os.path.exists( self.info.repodir ) ):
            os.makedirs( self.info.repodir )
        else:
            self.warning( "svn checkout destination already exists" )
        
        currentdir = self.info.repodir
        self.currentsvnpath = ""
        os.chdir( self.info.repodir )
        
        for tmpdir in self.info.svnpath.split( '/' )[:-1]:
            currentdir = os.path.join( currentdir, tmpdir )
            self.currentsvnpath += tmpdir
            if not self.__atomicCheckout():
                return False
            self.currentsvnpath += '/'
            os.chdir( currentdir )
        self.currentsvnpath = self.info.svnpath
        if not self.__atomicCheckout( True ):
            return False
        return True
    
    def update( self ):
        """ update local copy """
        if ( not self.localCopyExists() ):
            self.error( "svn update destination directory not existing." )
            return False
        os.chdir( self.info.repodir )
        
        currentdir = self.info.repodir
        self.currentsvnpath = ""
        os.chdir( self.info.repodir )
        
        for target in self.info.svnpath.split( '/' )[ :-1 ]:
            if self.verbose() > 2:
                print "target: ", target
            currentdir = os.path.join( currentdir, target )
            self.currentsvnpath += target
            if not self.__atomicUpdate( target ):
                self.error( 'failed on target: %s' % target )
                return False
            self.currentsvnpath += '/'
            os.chdir( currentdir )
        self.currentsvnpath = os.path.join( self.info.repodir, self.info.svnpath.replace( '/', os.path.sep ) )
        if self.verbose() > 2:
            print "target: ", self.info.svnpath.split( '/' )[ -1 ]
        if not self.__atomicUpdate( self.info.svnpath.split( '/' )[ -1 ], recursive=True ):
            return False
        return True
        
    def status( self ):
        """ check for status """
        """ it will return False if the repository is somehow locked """
        
        target = self.info.svnpath.split( '/' )[ -1 ]
        if ( self.localCopyExists() ):
            # this rather strange line removes the target (the last part of the svnpath) from the svnpath, translates it to a normal path and appends it to the repodir
            os.chdir( os.path.join( self.info.repodir, self.info.svnpath[:-(len(target) + 1)].replace('/', os.path.sep ) ) )
            if not self.isSvnRepo():
                self.warning( "svn destination directory %s is no valid svn directory" % ( self.info.repodir ) )
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
        if ".svn" not in os.listdir( os.path.join( self.info.repodir, self.info.svnpath.replace('/', os.path.sep ) ) ):
            return False
        else:
            return True
            
    def localCopyExists( self ):
        if ( not os.path.exists( os.path.join( self.info.repodir, self.info.svnpath.replace('/', os.path.sep ) ) ) ):
            return False
        else:
            return True
    
    def cleanup( self ):
        """ eventually cleanup the local copy """
        target = self.info.svnpath.split( '/' )[ -1 ]
        if ( self.localCopyExists() ):
            os.chdir( os.path.join( self.info.repodir, self.info.svnpath.replace('/' + target, '').replace('/', os.path.sep ) ) )
            
            if not self.isSvnRepo():
                self.warning( "svn destination directory is no valid svn directory" )
                return False
                
            command = "svn cleanup %s" % target
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
        else:
            self.warning( "svn destination directory not existing." )
            return False
        
    
    def runSelfTests( self ):
        """ define some tests to make sure this class works """
        
        self.info.repodir = "D:\\sources\\subversiontest"
        self.info.svnpath = "trunk/kdesupport/emerge"
        self.verb="2"
        
        print "checkout: ..."
        self.checkout()
        print "checkout done"
        print "status: ..."
        self.status()
        print "status done"
        print "cleanup: ..."
        self.cleanup()
        print "cleanup done"
        print "update: ..."
        self.update()
        print "update done"
        
        
if __name__ == '__main__':
    repository().runSelfTests()
