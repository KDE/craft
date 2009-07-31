# -*- coding: utf-8 -*-
"""@package provides cmake build system"""

import os
import utils

import base
import info

from BuildSystemBase import *

class CMakeBuildSystem(BuildSystemBase):
    """ cmake build support """
    def __init__( self, configureOptions="",makeOptions=""):
        """constructor. configureOptions are added to the configure command line and makeOptions are added to the make command line"""
        BuildSystemBase.__init__(self,"cmake",configureOptions,makeOptions)

        if self.compiler() == "msvc2005" or self.compiler() == "msvc2008":
            self.cmakeMakefileGenerator = "NMake Makefiles"
            self.cmakeMakeProgramm = "nmake"
        elif self.compiler() == "mingw":
            self.cmakeMakefileGenerator = "MinGW Makefiles"
            self.cmakeMakeProgramm = "mingw32-make"
        else:
            utils.die( "unknown %s compiler" % self.compiler() )
                                
    def configureDefaultDefines( self ):
        """returns default configure options"""
        sourcedir = self.configureSourceDir()
        ## \todo should install prefix not be set to mergeDir ?`
        options = "\"%s\" -DCMAKE_INSTALL_PREFIX=\"%s\" " % \
              ( sourcedir, self.mergeDestinationDir().replace( "\\", "/" ) )

        options = options + "-DCMAKE_INCLUDE_PATH=\"%s\" " % \
                os.path.join( self.mergeDestinationDir(), "include" ).replace( "\\", "/" )

        options = options + "-DCMAKE_LIBRARY_PATH=\"%s\" " % \
                os.path.join( self.mergeDestinationDir(), "lib" ).replace( "\\", "/" )

        if( not self.buildType() == None ):
            options  = options + "-DCMAKE_BUILD_TYPE=%s" % self.buildType()             
                
        return options

    def configure( self, buildType=None, customDefines="" ):
        """Using cmake"""

        ## \todo isn't builddir already cleaed on unpack ?
        if not self.noClean:
            utils.cleanDirectory( self.buildDir() )
            
        self.enterBuildDir()
        
        defines = self.configureDefaultDefines()
        
        command = r"""cmake -G "%s" %s %s""" % \
              ( self.cmakeMakefileGenerator, \
                defines, \
                self.configureOptions )

        if utils.verbose() > 0:
            print "configuration command: %s" % command
        utils.system( command ) or utils.die( "while CMake'ing. cmd: %s" % command )
        return True

    def make( self, buildType=None ):
        """run the *make program"""

        self.enterBuildDir()
        
        command = self.cmakeMakeProgramm

        if utils.verbose() > 1:
            command += " VERBOSE=1"
        
        command += ' %s' % self.makeOptions

        utils.system( command ) or utils.die( "while Make'ing. cmd: %s" % command )
        return True

    def install( self):
        """Using *make install"""

        self.enterBuildDir()

        #fastString = ""
        #if not self.noFast:
        #    fastString = "/fast"
        #command = "%s DESTDIR=%s install%s" % ( self.cmakeMakeProgramm, self.imageDir(), fastString )
        
        command = "cmake -DCMAKE_INSTALL_PREFIX=%s -P cmake_install.cmake" % self.installDir()
        
        utils.debug(command,1)
        utils.system( command ) or utils.die( "while installing. cmd: %s" % command )
        return True

    def runTest( self ):
        """running cmake based unittests"""

        self.enterbuildDir()

        if utils.verbose() > 0:
            print "builddir: " + builddir

        utils.system( "%s test" % ( self.cmakeMakeProgramm ) ) or utils.die( "while testing. cmd: %s" % "%s test" % ( self.cmakeMakeProgramm ) )
        return True
