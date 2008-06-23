# a python package which contains some helper classes and which should replace utils in the long run

import os
import sys
import imp
import subprocess

globalVerboseLevel = int( os.getenv( "EMERGE_VERBOSE" ) )

class Verbose:
    """ This class will work on the overall output verbosity """
    """ It defines the interface for the option parser but before the default value is taken """
    """ from the environment variable """

    def increase( self, option, opt, value, parser ):
        """ callback function as requested by the optparse parser """
        global globalVerboseLevel
        print "increase"
        globalVerboseLevel += 1
        self.VERBOSE = str( globalVerboseLevel )

    def decrease( self, option, opt, value, parser ):
        """ callback function as requested by the optparse parser """
        global globalVerboseLevel
        print "decrease"
        if globalVerboseLevel > 0:
            globalVerboseLevel -= 1
            self.VERBOSE = str( globalVerboseLevel )
            
    def setVerboseLevel( self, newLevel ):
        """ set the level by hand for quick and dirty changes """
        global globalVerboseLevel
        globalVerboseLevel = newLevel
        
    def verbose( self ):
        """ returns the verbosity level for the application """
        global globalVerboseLevel
        return globalVerboseLevel

class Environment ( Verbose ):
    def __init__( self ):
        """ """
#        Verbose.__init__( self )
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
        self.KDEROOT = other.KDEROOT
        self.LOGFILE = other.LOGFILE
        self.BUILDTYPE = other.BUILDTYPE
        self.BUILDTESTS = other.BUILDTESTS
        self.PKG_DEST_DIR = other.PKG_DEST_DIR
        self.COMPILER = other.COMPILER
        
class Object ( Environment ):
    def __init__( self ):
        """ """
        Environment.__init__( self )
        
    def inform( self, message ):
        if self.verbose() > 0:
            print "emerge info: %s" % message
        return True
        
    def debug( self, message, level=1 ):
        if self.verbose() > level:
            print "emerge debug: %s" % message
        return True
    
    def warning( self, message ):
        if self.verbose() > 0:
            print "emerge warning: %s" % message
        return True

    def error( self, message=None ):
        if not message:
            message = self.errormessage
        if self.verbose() > 0:
            print >> sys.stderr, "emerge error: %s" % message
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
        
    def __import__( self, module ):
        if not os.path.isfile( module ):
            return __builtin__.__import__( module )
        else:
            sys.path.append( os.path.dirname( module ) )
            fileHdl = open( module )
            modulename = os.path.basename( module ).replace('.py', '')
            return imp.load_module( modulename.replace('.', '_'), fileHdl, module, imp.get_suffixes()[1] )

