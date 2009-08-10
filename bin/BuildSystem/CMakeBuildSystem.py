# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

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

    def __onlyBuildDefines( self, buildOnlyTargets ):
        """This method returns a list of cmake defines to exclude targets from build""" 
        defines = ""
        sourceDir = self.sourceDir()
        topLevelCMakeList = os.path.join(self.sourceDir(),"CMakeLists.txt")
        if os.path.exists(topLevelCMakeList):
            f = open(topLevelCMakeList,'r')
            lines = f.read().splitlines()
            f.close()
            for line in lines:
                if line.find("macro_optional_add_subdirectory") > -1:
                    a = line.split("(")
                    a = a[1].split(")")
                    subdir = a[0].strip()
                    if not subdir in buildOnlyTargets:
                        defines += " -DBUILD_%s=OFF" % subdir
        #print defines
        return defines

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

        if self.subinfo.options.configure.onlyBuildTargets :
            defines += self.__onlyBuildDefines(self.subinfo.options.configure.onlyBuildTargets )
                
        if self.envPath <> '':
            utils.debug("adding %s to system path" % os.path.join( self.rootdir, self.envPath ),2)
            os.putenv( "PATH", os.path.join( self.rootdir, self.envPath ) + ";" + os.getenv("PATH") )
        
        command = r"""cmake -G "%s" %s %s""" % \
              ( self.cmakeMakefileGenerator, \
                defines, \
                self.configureOptions )

        return self.system( command, "configure", 0 ) 

    def make( self ):
        """run the *make program"""

        self.enterBuildDir()
        if self.envPath <> '':
            utils.debug("adding %s to system path" % os.path.join( self.rootdir, self.envPath ),2)
            os.putenv( "PATH", os.path.join( self.rootdir, self.envPath ) + ";" + os.getenv("PATH") )
        
        command = self.makeProgramm

        if utils.verbose() > 1:
            command += " VERBOSE=1"
        
        if self.subinfo.options.make.ignoreErrors:
            command += " -i"
            
        if self.subinfo.options.make.makeOptions:
            command += " %s" % self.subinfo.options.make.makeOptions

        return self.system( command, "make" ) 

    def install( self):
        """install the target"""

        self.enterBuildDir()
        
        fastString = ""
        if not self.noFast:
            fastString = "/fast"

        if self.subinfo.options.install.useMakeToolForInstall == True:          
            command = "%s DESTDIR=%s install%s" % ( self.makeProgramm, self.installDir(), fastString )
        else:
            command = "cmake -DCMAKE_INSTALL_PREFIX=%s -P cmake_install.cmake" % self.installDir()
        
        self.system( command, "install" ) 

        if self.subinfo.options.install.useMakeToolForInstall == True:
            utils.fixCmakeImageDir( self.installDir(), self.mergeDestinationDir() )
        return True

    def runTest( self ):
        """running cmake based unittests"""

        self.enterbuildDir()

        return self.system( "%s test" % ( self.cmakeMakeProgramm ), "test" )
