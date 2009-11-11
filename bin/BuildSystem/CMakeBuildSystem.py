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
    def __init__( self ):
        """constructor. configureOptions are added to the configure command line and makeOptions are added to the make command line"""
        BuildSystemBase.__init__(self,"cmake")

        if self.compiler() == "msvc2008":
            if self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE:
                self.cmakeMakefileGenerator = "Visual Studio 9 2008"            
            else:
                self.cmakeMakefileGenerator = "NMake Makefiles"
        elif self.compiler() == "msvc2005":                
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
    
    def __slnFileName(self):
        """ return solution file name """
        slnPackage = "%s.sln" % self.package
        if os.path.exists(os.path.join(self.buildDir(),slnPackage)):
            return slnPackage
        topLevelCMakeList = os.path.join(self.sourceDir(),"CMakeLists.txt")
        if os.path.exists(topLevelCMakeList):
            f = open(topLevelCMakeList,'r')
            lines = f.read().splitlines()
            f.close()
            for line in lines:
                if line.find("project(") > -1:
                    a = line.split("(")
                    a = a[1].split(")")
                    slnname = a[0].strip()
        if slnname:
            return "%s.sln" % slnname
        if self.subinfo.options.make.slnBaseName:
            return "%s.sln" % self.subinfo.options.make.slnBaseName
        return ""
 
    def configureOptions( self, defines=""):
        """returns default configure options"""
        options = BuildSystemBase.configureOptions(self)
        
        ## \todo why is it required to replace \\ by / ? 
        options += " -DCMAKE_INSTALL_PREFIX=\"%s\"" % self.mergeDestinationDir().replace( "\\", "/" )

        options += " -DCMAKE_INCLUDE_PATH=\"%s\"" % \
            os.path.join( self.mergeDestinationDir(), "include" ).replace( "\\", "/" )

        options += " -DCMAKE_LIBRARY_PATH=\"%s\"" % \
            os.path.join( self.mergeDestinationDir(), "lib" ).replace( "\\", "/" )

        if( not self.buildType() == None ):
            options += " -DCMAKE_BUILD_TYPE=%s" % self.buildType()             

        if not self.subinfo.options.configure.testDefine == None and "EMERGE_BUILDTESTS" in os.environ and os.environ["EMERGE_BUILDTESTS"] == "True" :
            print self.subinfo.options.configure.testDefine
            defines += self.subinfo.options.configure.testDefine
        if self.subinfo.options.configure.onlyBuildTargets :
            defines += self.__onlyBuildDefines(self.subinfo.options.configure.onlyBuildTargets )
                
        options += " \"%s\"" % self.configureSourceDir()
        return options

    def configure( self, defines=""):
        """implements configure step for cmake projects"""

        self.enterBuildDir()
            
        if self.envPath <> '':
            utils.debug("adding %s to system path" % os.path.join( self.rootdir, self.envPath ),2)
            os.putenv( "PATH", os.path.join( self.rootdir, self.envPath ) + ";" + os.getenv("PATH") )
        
        command = r"""cmake -G "%s" %s""" % (self.cmakeMakefileGenerator, self.configureOptions(defines) )

        return self.system( command, "configure", 0 ) 

    def make( self ):
        """implements the make step for cmake projects"""

        self.enterBuildDir()
        if self.envPath <> '':
            utils.debug("adding %s to system path" % os.path.join( self.rootdir, self.envPath ),2)
            os.putenv( "PATH", os.path.join( self.rootdir, self.envPath ) + ";" + os.getenv("PATH") )

        if self.compiler() == "msvc2008" and self.subinfo.options.cmake.openIDE:
            command = "start %s" % self.__slnFileName()             
        elif self.compiler() == "msvc2008" and self.subinfo.options.cmake.useIDE:
            command = "vcbuild /M2 %s \"%s|Win32\"" % (self.__slnFileName(),self.buildType())
        else:
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
            if self.compiler() == "msvc2008" and (self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE):
                command = "vcbuild INSTALL.vcproj \"%s|Win32\"" % self.buildType()
            else:
                command = "%s DESTDIR=%s install%s" % ( self.makeProgramm, self.installDir(), fastString )
        else:
            command = "cmake -DCMAKE_INSTALL_PREFIX=%s -P cmake_install.cmake" % self.installDir()
        
        self.system( command, "install" ) 

        if self.subinfo.options.install.useMakeToolForInstall == True and not (self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE):        
            utils.fixCmakeImageDir( self.installDir(), self.mergeDestinationDir() )
        return True

    def unittest( self ):
        """running cmake based unittests"""

        self.enterBuildDir()

        return self.system( "%s test" % ( self.makeProgramm ), "test" )
