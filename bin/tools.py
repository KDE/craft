# a python package which contains some helper classes and which should replace utils in the long run

import os
import sys
import subprocess

class emerge_environment:
    def __init__( self ):
        """ """
        self.VERBOSE = os.getenv( "EMERGE_VERBOSE" )
        self.KDEROOT = os.getenv( "KDEROOT" )
        self.LOGFILE = os.getenv( "EMERGE_LOGFILE" )
        self.BUILDTYPE = os.getenv( "EMERGE_BUILDTYPE" )
        self.BUILDTESTS = os.getenv( "EMERGE_BUILDTESTS" )
        self.PKG_DEST_DIR = os.getenv( "EMERGE_PKGDSTDIR" )
        self.COMPILER = os.getenv( "KDECOMPILER" )
        self.IGNORE_SUBVERSION = ".svn"
        if not self.LOGFILE:
            self.LOGFILE = '%KDEROOT%\\emerge-system.log'

        
    def __lshift__( self, other ):
        """ self << other """
        self.VERBOSE = other.VERBOSE
        self.KDEROOT = other.KDEROOT
        self.LOGFILE = other.LOGFILE
        self.BUILDTYPE = other.BUILDTYPE
        self.BUILDTESTS = other.BUILDTESTS
        self.PKG_DEST_DIR = other.PKG_DEST_DIR
        self.COMPILER = other.COMPILER
        
class emerge_container ( emerge_environment ):
    def __init__( self ):
        """ """
        emerge_environment.__init__( self )
    
    def verbose( self ):
        """ returns the verbose level for the application """
        if ( not self.VERBOSE == None and self.VERBOSE.isdigit() and int( self.VERBOSE ) > 0 ):
            return int( self.VERBOSE )
        else:
            return 0
        
    def warning( self, message ):
        if self.verbose() > 0:
            print "emerge warning: %s" % message
        return True

    def error( self, message=None ):
        if not message:
            message = self.errormessage
        if self.verbose() > 0:
            print "emerge error: %s" % message
        return False
        
    def die( self, message ):
        print "emerge fatal error: %s" % message
        exit( 1 )

    def system( self, cmdstring, die=False, capture_output=None ):
        if self.verbose() == 0:
            self.stderr = file( self.LOGFILE, 'wb' )
            self.stdout = sys.stderr
        else:
            self.stderr = sys.stderr
            self.stdout = sys.stdout
        if capture_output:
            self.stderr = capture_output
            self.stdout = capture_output
        if self.verbose() > 1:
            print "system() executing this: <" + cmdstring + ">"
        p = subprocess.Popen( cmdstring, shell=True, stdout=self.stdout, stderr=self.stderr )
        ret = p.wait()
        if die:
            self.die( "system failed to execute: <" + cmdstring + ">" )
        return ret

class portage( emerge_environment ):
    def __init__( self ):
        """ ctor """
        emerge_environment.__init__( self )
        self.PORTAGE_DIRS = []
        if os.getenv( "EMERGE_PORTAGE_DIRS" ):
            for i in os.getenv( "EMERGE_PORTAGE_DIRS" ).split( os.pathsep ):
                self.PORTAGE_DIRS.append( i )
        self.PORTAGE_DIRS.append( os.path.join( self.KDEROOT, "emerge", "portage" ) )
        
    def sync( self ):
        """ sync the portage directory(ies) """
        for portage_dir in self.PORTAGE_DIRS:
            print portage_dir
        
    def list_packages( self ):
        """ return a list of all packages including the category, name, version and path of the script """
        instList = []
        for portage_dir in self.PORTAGE_DIRS:
            catdirs = os.listdir( portage_dir )

            for category in catdirs:
                if os.path.isdir( os.path.join( portage_dir, category ) ):
                    pakdirs = os.listdir( os.path.join( portage_dir, category ) )
                    if self.IGNORE_SUBVERSION in pakdirs:
                        pakdirs.remove( self.IGNORE_SUBVERSION )
                    for package in pakdirs:
                        if os.path.isdir( os.path.join( portage_dir, category, package ) ):
                            scriptdirs = os.listdir( os.path.join( portage_dir, category, package ) )
                            for script in scriptdirs:
                                if script.endswith( '.py' ):
                                    version = script.replace('.py', '').replace(package + '-', '')
                                    instList.append( [ category, package, os.path.join( portage_dir, category, package, script), version ] )

        return instList
        
