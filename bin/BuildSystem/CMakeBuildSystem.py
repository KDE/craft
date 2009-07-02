# -*- coding: utf-8 -*-
# definitions for the cmake build system

import os
import utils

import base
import info

from BuildSystemBase import *

class CMakeBuildSystem(BuildSystemBase):
    def __init__( self, env = dict( os.environ ) ):
        BuildSystemBase.__init__(self)

    def svnPath(self): 
        return ""
                                
    def configureDefaultDefines( self ):
        """defining the default cmake cmd line"""
        options = "\"%s\" -DCMAKE_INSTALL_PREFIX=\"%s\" " % \
              ( self.sourcedir, self.rootdir.replace( "\\", "/" ) )

        options = options + "-DCMAKE_INCLUDE_PATH=\"%s\" " % \
                os.path.join( self.rootdir, "include" ).replace( "\\", "/" )

        options = options + "-DCMAKE_LIBRARY_PATH=\"%s\" " % \
                os.path.join( self.rootdir, "lib" ).replace( "\\", "/" )

        if( not self.buildType == None ):
            options  = options + "-DCMAKE_BUILD_TYPE=%s" % self.buildType             
                
        return options

    def configure( self, buildType=None, customDefines="" ):
        """Using cmake"""
            
        self.enterBuildDir()
        
        if not self.noClean:
            utils.cleanDirectory( self.builddir )

        command = r"""cmake -G "%s" %s %s""" % \
              ( self.cmakeMakefileGenerator, \
                self.configureDefaultDefines(), \
                customDefines )

        if utils.verbose() > 0:
            print "configuration command: %s" % command
        utils.system( command ) or utils.die( "while CMake'ing. cmd: %s" % command )
        return True

    def make( self, buildType=None ):
        """Using the *make program"""
        builddir = "%s" % ( self.COMPILER )

        if( buildType == None ):
            buildType = self.buildType
        
        # todo fixes buildtype and buildType spelling issues 
        if( not buildType == None ):
            builddir = "%s-%s" % ( builddir, buildType )
            
        if( not self.buildNameExt == None ):
            builddir = "%s-%s" % ( builddir, self.buildNameExt )

        os.chdir( os.path.join( self.workdir, builddir ) )
        command = self.cmakeMakeProgramm
        # adding Targets later
        if utils.verbose() > 1:
            command += " VERBOSE=1"
        utils.system( command ) or utils.die( "while Make'ing. cmd: %s" % command )
        return True

    def __install( self, buildType=None ):
        """Using *make install"""
        builddir = "%s" % ( self.COMPILER )

        if( buildType == None ):
            buildType = self.buildType
        
        if( not buildType == None ):
            builddir = "%s-%s" % ( builddir, buildType )

        if( not self.buildNameExt == None ):
            builddir = "%s-%s" % ( builddir, self.buildNameExt )

        os.chdir( self.workdir )
        os.chdir( builddir )

        if utils.verbose() > 0:
            print "builddir: " + builddir

        fastString = ""
        if not self.noFast:
            fastString = "/fast"
        utils.system( "%s DESTDIR=%s install%s" % ( self.cmakeMakeProgramm, self.imagedir, fastString ) ) or utils.die( "while installing. cmd: %s" % "%s DESTDIR=%s install" % ( self.cmakeMakeProgramm , self.imagedir ) )
        return True

    def compile( self, customDefines=""):
        """making all required stuff for compiling cmake based modules"""
        if( not self.buildType == None ) :
            if( not ( self.configure( self.buildType, customDefines ) and self.make( self.buildType ) ) ):
                return False
        else:
            if( not ( self.configure( "Debug", customDefines ) and self.make( "Debug" ) ) ):
                return False
            if( not ( self.configure( "Release", customDefines ) and self.make( "Release" ) ) ):
                return False
        return True

    def install( self ):
        """making all required stuff for installing cmake based modules"""
        if( not self.buildType == None ):
            if( not self.__install( self.buildType ) ):
                return False
        else:
            if( not self.__install( "debug" ) ):
                return False
            if( not self.__install( "release" ) ):
                return False
        utils.fixCmakeImageDir( self.imagedir, self.rootdir )
        return True

    def runTest( self ):
        """running cmake based unittests"""
        builddir = "%s" % ( self.COMPILER )

        if( not self.buildType == None ):
            builddir = "%s-%s" % ( builddir, self.buildType )

        if( not self.buildNameExt == None ):
            builddir = "%s-%s" % ( builddir, self.buildNameExt )

        os.chdir( self.workdir )
        os.chdir( builddir )

        if utils.verbose() > 0:
            print "builddir: " + builddir

        utils.system( "%s test" % ( self.cmakeMakeProgramm ) ) or utils.die( "while testing. cmd: %s" % "%s test" % ( self.cmakeMakeProgramm ) )
        return True
