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
        elif self.compiler() == "mingw" or self.compiler() == "mingw4":
            self.cmakeMakefileGenerator = "MinGW Makefiles"
        else:
            utils.die( "unknown %s compiler" % self.compiler() )
                                
    def configureDefaultDefines( self ):
        """returns default configure options"""
        sourcedir = self.configureSourceDir()
        options = "\"%s\" -DCMAKE_INSTALL_PREFIX=\"%s\" " % \
              ( sourcedir, self.mergeDestinationDir().replace( "\\", "/" ) )

        options = options + "-DCMAKE_INCLUDE_PATH=\"%s\" " % \
                os.path.join( self.mergeDestinationDir(), "include" ).replace( "\\", "/" )

        options = options + "-DCMAKE_LIBRARY_PATH=\"%s\" " % \
                os.path.join( self.mergeDestinationDir(), "lib" ).replace( "\\", "/" )

        if( not self.buildType() == None ):
            options  = options + "-DCMAKE_BUILD_TYPE=%s" % self.buildType()             
                
        return options

    def configure( self ):
        """Using cmake"""

        self.enterBuildDir()
        
        defines = self.configureDefaultDefines()
        if not self.subinfo.options.configure.defines == None:
            defines += " %s" % self.subinfo.options.configure.defines
            
        if self.envPath <> '':
            utils.debug("adding %s to system path" % os.path.join( self.rootdir, self.envPath ),2)
            os.putenv( "PATH", os.path.join( self.rootdir, self.envPath ) + ";" + os.getenv("PATH") )
        
        command = r"""cmake -G "%s" %s %s""" % \
              ( self.cmakeMakefileGenerator, \
                defines, \
                self.configureOptions )

        #utils.debug("cofigure command: %s" % command,1)
        utils.system( command ) or utils.die( "while configuring. cmd: %s" % command )
        return True

    def make( self ):
        """run the *make program"""

        self.enterBuildDir()
        if self.envPath <> '':
            utils.debug("adding %s to system path" % os.path.join( self.rootdir, self.envPath ),2)
            os.putenv( "PATH", os.path.join( self.rootdir, self.envPath ) + ";" + os.getenv("PATH") )
        
        command = self.makeProgramm

        if utils.verbose() > 1:
            command += " VERBOSE=1"
        
        command += ' %s' % self.makeOptions

        utils.system( command ) or utils.die( "while Make'ing. cmd: %s" % command )
        return True

    def install( self):
        """Using *make install"""

        self.enterBuildDir()
        
        fastString = ""
        if not self.noFast:
            fastString = "/fast"

        if self.subinfo.options.install.useMakeToolForInstall == True:          
            # \todo is installDir() here not the right choice ? 
            command = "%s DESTDIR=%s install%s" % ( self.makeProgramm, self.imageDir(), fastString )
        else:
            command = "cmake -DCMAKE_INSTALL_PREFIX=%s -P cmake_install.cmake" % self.installDir()
        
        print command
        utils.debug(command,1)
        utils.system( command ) or utils.die( "while installing. cmd: %s" % command )

        if self.subinfo.options.install.useMakeToolForInstall == True:
            # \todo is installDir() here not the right choice ? 
	        utils.fixCmakeImageDir( self.imageDir(), self.mergeDestinationDir() )
        return True

    def runTest( self ):
        """running cmake based unittests"""

        self.enterbuildDir()

        utils.system( "%s test" % ( self.cmakeMakeProgramm ) ) or utils.die( "while testing. cmd: %s" % "%s test" % ( self.cmakeMakeProgramm ) )
        return True
