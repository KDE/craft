# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

"""@package provides cmake build system"""

import os
import utils

import base
import info
import compiler
import compilercache
from CMakeDependencies import *

from BuildSystemBase import *

class CMakeBuildSystem(BuildSystemBase):
    """ cmake build support """
    def __init__( self ):
        """constructor. configureOptions are added to the configure command line and makeOptions are added to the make command line"""
        BuildSystemBase.__init__(self,"cmake")

    def __makeFileGenerator(self):
        """return cmake related make file generator"""
        if self.compiler() == "msvc2008":
            if self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE:
                if self.isTargetBuild():
                    return "Visual Studio 9.0 Windows Mobile 6 Professional SDK (ARMV4I)"  
                else:
                    return "Visual Studio 9 2008"            
            else:
                return "NMake Makefiles"
        elif self.compiler() == "msvc2005" or self.compiler() == "msvc2010":                
            return "NMake Makefiles"
        elif self.compiler() == "mingw" or self.compiler() == "mingw4":
            return "MinGW Makefiles"
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
        slnname = "%s.sln" % self.package
        if os.path.exists(os.path.join(self.buildDir(),slnname)):
            return slnname
        topLevelCMakeList = os.path.join(self.configureSourceDir(),"CMakeLists.txt")
        if os.path.exists(topLevelCMakeList):
            f = open(topLevelCMakeList,'r')
            lines = f.read().splitlines()
            f.close()
            for line in lines:
                if line.find("project(") > -1:
                    a = line.split("(")
                    a = a[1].split(")")
                    slnname = "%s.sln" % a[0].strip()                    
        if os.path.exists(os.path.join(self.buildDir(),slnname)):
            return slnname
        slnname = "%s.sln" % self.subinfo.options.make.slnBaseName
        if os.path.exists(os.path.join(self.buildDir(),slnname)):
            return slnname
        return "NO_NAME_FOUND"
 
    def configureOptions( self, defines=""):
        """returns default configure options"""
        options = BuildSystemBase.configureOptions(self)
        
        ## \todo why is it required to replace \\ by / ? 
        options += compilercache.getCMakeArguments()
        options += " -DCMAKE_INSTALL_PREFIX=\"%s\"" % self.mergeDestinationDir().replace( "\\", "/" )

        options += " -DCMAKE_INCLUDE_PATH=\"%s\"" % \
            os.path.join( self.mergeDestinationDir(), "include" ).replace( "\\", "/" )

        options += " -DCMAKE_LIBRARY_PATH=\"%s\"" % \
            os.path.join( self.mergeDestinationDir(), "lib" ).replace( "\\", "/" )
            
        options += " -DCMAKE_PREFIX_PATH=\"%s\"" % \
            self.mergeDestinationDir().replace( "\\", "/" )

        if( not self.buildType() == None ):
            options += " -DCMAKE_BUILD_TYPE=%s" % self.buildType()             
            
        if self.buildPlatform() == "WM60" or self.buildPlatform() == "WM65":
            options += " -DCMAKE_SYSTEM_NAME=WinCE -DCMAKE_SYSTEM_VERSION=5.02"
        elif self.buildPlatform() == "WM50":
            options += " -DCMAKE_SYSTEM_NAME=WinCE -DCMAKE_SYSTEM_VERSION=5.01"

        if self.buildTests:
            # @todo KDE4_BUILD_TESTS is only required for kde packages, how to detect this case 
            options += " -DKDE4_BUILD_TESTS=1 "
            if not self.subinfo.options.configure.testDefine == None:
                options += self.subinfo.options.configure.testDefine
        if self.subinfo.options.configure.onlyBuildTargets :
            options += self.__onlyBuildDefines(self.subinfo.options.configure.onlyBuildTargets )
        if self.subinfo.options.cmake.useCTest:
            options += " -DCMAKE_PROGRAM_PATH=\"%s\" " % \
                            ( os.path.join( self.mergeDestinationDir(), "dev-utils", "svn", "bin" ).replace( "\\", "/" ) )
        options += " \"%s\"" % self.configureSourceDir()
        return options

    def configure( self, defines=""):
        """implements configure step for cmake projects"""

        self.enterBuildDir()
            
        if self.envPath <> '':
            utils.debug("adding %s to system path" % os.path.join( self.rootdir, self.envPath ),2)
            os.putenv( "PATH", os.path.join( self.rootdir, self.envPath ) + ";" + os.getenv("PATH") )
        
        command = r"""cmake -G "%s" %s""" % (self.__makeFileGenerator(), self.configureOptions(defines) )

        fc = open(os.path.join(self.buildDir(), "cmake-command.bat"), "w")
        fc.write(command);
        fc.close()

        if self.isTargetBuild():
            self.setupTargetToolchain()

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
            if self.isTargetBuild():
                command = "vcbuild /M1 %s \"%s|Windows Mobile 6 Professional SDK (ARMV4I)\"" % (self.__slnFileName(),self.buildType())
            else:
                command = "vcbuild /M1 %s \"%s|WIN32\"" % (self.__slnFileName(),self.buildType())
        elif self.subinfo.options.cmake.useCTest:
            # first make clean
            self.system( self.makeProgramm + " clean", "make clean" ) 
            command = "ctest -M " + "Nightly" + " -T Start -T Update -T Configure -T Build -T Submit"
        else:
            command = self.makeProgramm

            if utils.verbose() > 1:
                command += " VERBOSE=1"
            
            if self.subinfo.options.make.ignoreErrors:
                command += " -i"
                
            if self.subinfo.options.make.makeOptions:
                command += " %s" % self.subinfo.options.make.makeOptions

        if self.isTargetBuild():
            self.setupTargetToolchain()

        return self.system( command, "make" ) 
        
    def install( self):
        """install the target"""
        self.enterBuildDir()
        
        fastString = ""
        if not self.noFast:
            fastString = "/fast"

        if self.subinfo.options.install.useMakeToolForInstall == True:          
            if self.compiler() == "msvc2008" and (self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE):
                if self.isTargetBuild():
                    command = "vcbuild INSTALL.vcproj \"%s|Windows Mobile 6 Professional SDK (ARMV4I)\"" % self.buildType()
                else:
                    command = "vcbuild INSTALL.vcproj \"%s|Win32\"" % self.buildType()
            else:
                command = "%s DESTDIR=%s install%s" % ( self.makeProgramm, self.installDir(), fastString )
        else:
            command = "cmake -DCMAKE_INSTALL_PREFIX=%s -P cmake_install.cmake" % self.installDir()

        if self.isTargetBuild():
            self.setupTargetToolchain()

        self.system( command, "install" ) 

        if self.subinfo.options.install.useMakeToolForInstall == True and not (self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE):        
            utils.fixCmakeImageDir( self.installDir(), self.mergeDestinationDir() )
        return True

    def unittest( self ):
        """running cmake based unittests"""

        self.enterBuildDir()

        return self.system( "%s test" % ( self.makeProgramm ), "test" )

    def dumpDependencies( self ):
        """dump package dependencies as pdf (requires installed dot)"""

        srcDir = self.sourceDir()
        outDir = self.buildDir()
        self.enterBuildDir()
        outFile = os.path.join(outDir,self.package+'.dot')
        a = CMakeDependencies(self)
        if not a.parse(srcDir): 
            utils.debug("could not find source files",0)
            return False
        title = "%s cmake dependency chart - version %s" % (self.package, self.version)
        if not a.toDot(title,srcDir,outFile):
            return False

        if not a.runDot(outFile, 'pdf', outFile+'.pdf'):
            return false

        return a.openOutput(outFile+'.pdf')
           