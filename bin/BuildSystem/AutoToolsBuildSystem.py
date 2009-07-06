# -*- coding: utf-8 -*-
# definitions for the autotools build system

import os
import utils

import base
import info
from shells import *

from BuildSystemBase import *

class AutoToolsBuildSystem(BuildSystemBase):
    def __init__( self, env = dict( os.environ ) ):
        BuildSystemBase.__init__(self)
        self.shell = MSysShell()
            
    def configureDefaultDefines( self ):
        """defining the default cmake cmd line"""
        return ""

    def configure( self, buildType=None, customDefines="" ):
        """configure the target"""
            
        if not self.noClean:
            utils.cleanDirectory( self.builddir )

        self.enterBuildDir()

        #todo make generic
        ret = self.shell.execute(self.sourcedir, "ruby configure", "" )
        return ret

    def make( self, buildType=None ):
        """Using the *make program"""

        self.enterBuildDir()
        
        command = "make"
        args = "-j2"
        # adding Targets later
        if utils.verbose() > 1:
            args += " VERBOSE=1"
        self.shell.execute(self.sourcedir, command, args ) or utils.die( "while Make'ing. cmd: %s" % command )
        return True

    def __install( self, buildType=None ):
        """Using *make install"""

        self.enterBuildDir()
        
        fastString = ""
        if not self.noFast:
            fastString = "/fast"
        utils.system( "%s DESTDIR=%s install%s" % ( self.cmakeMakeProgramm, self.imageDir(), fastString ) ) or utils.die( "while installing. cmd: %s" % "%s DESTDIR=%s install" % ( self.cmakeMakeProgramm , self.imageDir() ) )
        return True

    def compile( self, customDefines=""):
        """making all required stuff for compiling cmake based modules"""
        if( not self.buildType() == None ) :
            if( not ( self.configure( self.buildType(), customDefines ) and self.make( self.buildType() ) ) ):
                return False
        else:
            if( not ( self.configure( "Debug", customDefines ) and self.make( "Debug" ) ) ):
                return False
            if( not ( self.configure( "Release", customDefines ) and self.make( "Release" ) ) ):
                return False
        return True

    def install( self ):
        """making all required stuff for installing cmake based modules"""
        if( not self.buildType() == None ):
            if( not self.__install( self.buildType() ) ):
                return False
        else:
            if( not self.__install( "debug" ) ):
                return False
            if( not self.__install( "release" ) ):
                return False
        utils.fixCmakeImageDir( self.imageDir(), self.rootdir )
        return True

    def runTest( self ):
        """running cmake based unittests"""

        self.enterBuildDir()
        
        if utils.verbose() > 0:
            print "builddir: " + builddir

        fastString = ""
        if not self.noFast:
            fastString = "/fast"
        utils.system( "%s test" % ( self.cmakeMakeProgramm ) ) or utils.die( "while testing. cmd: %s" % "%s test" % ( self.cmakeMakeProgramm ) )
        return True
