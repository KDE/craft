#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#

"""@package provides cmake build system"""

import os

import EmergeDebug
import utils
from BuildSystem.CMakeDependencies import *
from BuildSystem.BuildSystemBase import *
from graphviz import *
import compiler
import utils
from EmergeOS.osutils import OsUtils



class CMakeBuildSystem(BuildSystemBase):
    """ cmake build support """
    def __init__( self ):
        """constructor. configureOptions are added to the configure command line and makeOptions are added to the make command line"""
        BuildSystemBase.__init__(self, "cmake")
        self.supportsNinja = True

    def __makeFileGenerator(self):
        """return cmake related make file generator"""
        if self.supportsNinja and emergeSettings.getboolean("Compile","UseNinja", False):
            return "Ninja"
        if OsUtils.isWin():
            if compiler.isMSVC2015():
                if self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE:
                    return "Visual Studio 14 2015" + " Win64" if compiler.isX64() else ""
                else:
                    return "NMake Makefiles"
            if compiler.isMSVC2010():
                if self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE:
                    return "Visual Studio 10"
                else:
                    return "NMake Makefiles"
            elif compiler.isMSVC2008():
                if self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE:
                    return "Visual Studio 9 2008"
                else:
                    return "NMake Makefiles"
            elif compiler.isMSVC() or compiler.isIntel():
                return "NMake Makefiles"
            elif compiler.isMinGW():
                return "MinGW Makefiles"
        elif OsUtils.isUnix():
            return "Unix Makefiles"
        else:
            EmergeDebug.die("unknown %s compiler" % self.compiler())

    def __onlyBuildDefines( self, buildOnlyTargets ):
        """This method returns a list of cmake defines to exclude targets from build"""
        defines = ""
        topLevelCMakeList = os.path.join(self.sourceDir(), "CMakeLists.txt")
        if os.path.exists(topLevelCMakeList):
            with open(topLevelCMakeList,'r') as f:
                lines = f.read().splitlines()
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
        if os.path.exists(os.path.join(self.buildDir(), slnname)):
            return slnname
        topLevelCMakeList = os.path.join(self.configureSourceDir(), "CMakeLists.txt")
        if os.path.exists(topLevelCMakeList):
            with open(topLevelCMakeList,'r') as f:
                lines = f.read().splitlines()
            for line in lines:
                if line.find("project(") > -1:
                    a = line.split("(")
                    a = a[1].split(")")
                    slnname = "%s.sln" % a[0].strip()
        if os.path.exists(os.path.join(self.buildDir(), slnname)):
            return slnname
        slnname = "%s.sln" % self.subinfo.options.make.slnBaseName
        if os.path.exists(os.path.join(self.buildDir(), slnname)):
            return slnname
        return "NO_NAME_FOUND"

    def configureOptions( self, defines=""):
        """returns default configure options"""
        options = BuildSystemBase.configureOptions(self)

        ## \todo why is it required to replace \\ by / ?
        options += " -DCMAKE_INSTALL_PREFIX=\"%s\"" % self.mergeDestinationDir().replace( "\\", "/" )

        options += " -DCMAKE_PREFIX_PATH=\"%s\"" % \
            self.mergeDestinationDir().replace( "\\", "/" )

        if( not self.buildType() == None ):
            options += " -DCMAKE_BUILD_TYPE=%s" % self.buildType()

        if compiler.isGCC() and not compiler.isNative():
            options += " -DCMAKE_TOOLCHAIN_FILE=%s" % os.path.join( EmergeStandardDirs.emergeRoot(), "emerge", "bin", "toolchains", "Toolchain-cross-mingw32-linux-%s.cmake" % compiler.architecture())

        if OsUtils.isWin():
            options += " -DKDE_INSTALL_USE_QT_SYS_PATHS=ON"

        if OsUtils.isMac():
            options += " -DBUNDLE_INSTALL_DIR=\"%s/Applications/KDE\" -DAPPLE_SUPPRESS_X11_WARNING=ON" % \
                self.mergeDestinationDir().replace( "\\", "/" )

        if self.buildTests:
            # @todo KDE4_BUILD_TESTS is only required for kde packages, how to detect this case
            if not self.subinfo.options.configure.testDefine == None:
                options += " " + self.subinfo.options.configure.testDefine + " "
            else:
                options += " -DKDE4_BUILD_TESTS=1 "
        if self.subinfo.options.buildTools:
            options += " " + self.subinfo.options.configure.toolsDefine + " "
        if self.subinfo.options.buildStatic and self.subinfo.options.configure.staticDefine:
            options += " " + self.subinfo.options.configure.staticDefine + " "
        if self.subinfo.options.configure.onlyBuildTargets :
            options += self.__onlyBuildDefines(self.subinfo.options.configure.onlyBuildTargets )
        if self.subinfo.options.cmake.useCTest:
            options += " -DCMAKE_PROGRAM_PATH=\"%s\" " % \
                            ( os.path.join( self.mergeDestinationDir(), "dev-utils", "svn", "bin" ).replace( "\\", "/" ) )
        if compiler.isIntel():
            # this is needed because otherwise it'll detect the MSVC environment
            options += " -DCMAKE_CXX_COMPILER=\"%s\" " % os.path.join(os.getenv("BIN_ROOT"), os.getenv("ARCH_PATH"), "icl.exe" ).replace( "\\", "/" )
            options += " -DCMAKE_C_COMPILER=\"%s\" " % os.path.join(os.getenv("BIN_ROOT"), os.getenv("ARCH_PATH"), "icl.exe" ).replace( "\\", "/" )
            options += " -DCMAKE_LINKER=\"%s\" " % os.path.join(os.getenv("BIN_ROOT"), os.getenv("ARCH_PATH"), "xilink.exe" ).replace( "\\", "/" )
        options += " \"%s\"" % self.configureSourceDir()
        return options

    def configure( self, defines=""):
        """implements configure step for cmake projects"""

        self.enterBuildDir()
        command = r"""cmake -G "%s" %s""" % (self.__makeFileGenerator(), self.configureOptions(defines) )

        with open(os.path.join(self.buildDir(), "cmake-command.bat"), "w") as fc:
            fc.write(command)

        return self.system( command, "configure", 0 )

    def make( self ):
        """implements the make step for cmake projects"""

        self.enterBuildDir()

        if self.subinfo.options.cmake.openIDE:
            if compiler.isMSVC2008():
                command = "start %s" % self.__slnFileName()
            elif compiler.isMSVC2010():
                command = "start vcexpress %s" % self.__slnFileName()
        elif self.subinfo.options.cmake.useIDE:
            if compiler.isMSVC2008():
                command = "vcbuild /M1 %s \"%s|WIN32\"" % (self.__slnFileName(), self.buildType())
            elif compiler.isMSVC2015():
                command = "msbuild /maxcpucount %s /t:ALL_BUILD /p:Configuration=\"%s\"" % (self.__slnFileName(), self.buildType())
            elif compiler.isMSVC2010():
                EmergeDebug.die("has to be implemented");
        elif self.subinfo.options.cmake.useCTest:
            # first make clean
            self.system( self.makeProgramm + " clean", "make clean" )
            command = "ctest -M " + "Nightly" + " -T Start -T Update -T Configure -T Build -T Submit"
        else:
            command = ' '.join([self.makeProgramm, self.makeOptions()])


        return self.system( command, "make" )

    def install( self):
        """install the target"""
        if not BuildSystemBase.install(self):
            return False

        self.enterBuildDir()

        fastString = ""
        if not self.noFast:
            fastString = "/fast"

        if self.subinfo.options.install.useMakeToolForInstall:
            if compiler.isMSVC2008() and (self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE):
                command = "vcbuild INSTALL.vcproj \"%s|Win32\"" % self.buildType()
            elif compiler.isMSVC2015() and (self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE):
                command = "msbuild INSTALL.vcxproj /p:Configuration=\"%s\"" % self.buildType()
            else:
                os.putenv("DESTDIR",self.installDir())
                command = "%s install%s" % ( self.makeProgramm, fastString )
        else:
            command = "cmake -DCMAKE_INSTALL_PREFIX=%s -P cmake_install.cmake" % self.installDir()

        self.system( command, "install" )

        if self.subinfo.options.install.useMakeToolForInstall and not (self.subinfo.options.cmake.useIDE or self.subinfo.options.cmake.openIDE):
            self._fixCmakeImageDir(self.installDir(), self.mergeDestinationDir())
        return True

    def unittest( self ):
        """running cmake based unittests"""

        self.enterBuildDir()

        return self.system("ctest --output-on-failure")

    def dumpDependencies( self ):
        self.dumpCMakeDependencies()
        return self.dumpEmergeDependencies()

    def dumpCMakeDependencies(self):
        """dump package dependencies as pdf (requires installed dot)"""

        srcDir = self.sourceDir()
        outDir = self.buildDir()
        self.enterBuildDir()
        outFile = os.path.join(outDir, self.package+'-cmake.dot')
        a = CMakeDependencies()
        if not a.parse(srcDir):
            EmergeDebug.debug("could not find source files for generating cmake dependencies")
            return False
        title = "%s cmake dependency chart - version %s" % (self.package, self.version)
        a.toPackageList(title, srcDir)
        if not a.toDot(title, srcDir, outFile):
            EmergeDebug.debug("could not create dot file")
            return False

        graphviz = GraphViz(self)

        if not graphviz.runDot(outFile, outFile+'.pdf', 'pdf'):
            return False

        return graphviz.openOutput()

    def ccacheOptions(self):
        out  =  " -DCMAKE_CXX_COMPILER=ccache -DCMAKE_CXX_COMPILER_ARG1=g++ "
        out  += " -DCMAKE_C_COMPILER=ccache -DCMAKE_C_COMPILER_ARG1=gcc "
        return out

    def clangOptions(self):
        if compiler.isGCC():
            out  =  " -DCMAKE_CXX_COMPILER=clang++"
            out  += " -DCMAKE_C_COMPILER=clang"
        elif compiler.isMSVC():
            out = " -DCMAKE_CXX_COMPILER=clang-cl"
            out += " -DCMAKE_C_COMPILER=clang-cl"
        return out


    def _fixCmakeImageDir(self, imagedir, rootdir ):
        """
        when using DESTDIR=foo under windows, it does not _replace_
        CMAKE_INSTALL_PREFIX with it, but prepends destdir to it.
        so when we want to be able to install imagedir into KDEROOT,
        we have to move things around...
        """
        EmergeDebug.debug("fixImageDir: %s %s" % (imagedir, rootdir), 1)
        # imagedir = e:\foo\thirdroot\tmp\dbus-0\image
        # rootdir  = e:\foo\thirdroot
        # files are installed to
        # e:\foo\thirdroot\tmp\dbus-0\image\foo\thirdroot
        _, rootpath = os.path.splitdrive( rootdir )
        #print "rp:", rootpath
        if ( rootpath.startswith( os.path.sep ) ):
            rootpath = rootpath[1:]
        # CMAKE_INSTALL_PREFIX = X:\
        # -> files are installed to
        # x:\build\foo\dbus\image\
        # --> all fine in this case
        #print("rp:", rootpath)
        if len(rootpath) == 0:
            return

        tmp = os.path.join( imagedir, rootpath )
        EmergeDebug.debug("tmp: %s" % tmp, 1)
        tmpdir = os.path.join( imagedir, "tMpDiR" )
        if ( not os.path.isdir( tmpdir ) ):
            os.mkdir( tmpdir )
        utils.moveEntries( tmp, tmpdir )
        os.chdir( imagedir )
        os.removedirs( rootpath )
        utils.moveEntries( tmpdir, imagedir )
        utils.cleanDirectory( tmpdir )
        os.rmdir( tmpdir )
