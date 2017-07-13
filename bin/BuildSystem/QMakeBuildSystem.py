#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# definitions for the qmake build system
from CraftDebug import craftDebug
import utils
import compiler

from CraftOS.osutils import OsUtils

from BuildSystem.BuildSystemBase import *
from CraftVersion import CraftVersion


class QMakeBuildSystem(BuildSystemBase):
    def __init__( self ):
        BuildSystemBase.__init__(self, "qmake")
        self.platform = ""
        if OsUtils.isWin():
            if compiler.isMSVC():
                if compiler.isClang():
                    self.platform = "win32-clang-%s" % (self.compiler() if CraftVersion(self.subinfo.buildTarget) < CraftVersion("5.8") else "msvc")
                else:
                    self.platform = "win32-%s" % (self.compiler() if CraftVersion(self.subinfo.buildTarget) < CraftVersion("5.8") else "msvc")
            elif compiler.isMinGW():
                self.platform = "win32-g++"
            elif compiler.isIntel():
                self.platform = "win32-icc"
            else:
                craftDebug.log.critical("QMakeBuildSystem: unsupported compiler platform %s" % self.compiler())
        elif OsUtils.isUnix():
            if OsUtils.isMac():
                osPart = "macx"
            elif OsUtils.isFreeBSD():
                osPart = "freebsd"
            else:
                osPart = "linux"

            if compiler.isClang():
                compilerPart = "clang"
            else:
                compilerPart = "g++"
            self.platform = osPart + "-" + compilerPart

    def configure( self, configureDefines="" ):
        """inplements configure step for Qt projects"""
        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()

        proFile = self.configureSourceDir()
        if self.subinfo.options.configure.projectFile:
            proFile = os.path.join(self.configureSourceDir(), self.subinfo.options.configure.projectFile)
        command = "%s -makefile %s %s" % (utils.utilsCache.findApplication("qmake") , proFile, self.configureOptions(configureDefines))

        return self.system( command, "configure" )

    def make( self, options=""):
        """implements the make step for Qt projects"""
        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()
        command = ' '.join([self.makeProgram, self.makeOptions(options)])

        return self.system( command, "make" )

    def install( self, options=None ):
        """implements the make step for Qt projects"""
        if not BuildSystemBase.install(self):
            return False

        if OsUtils.isWin():
            # There is a bug in jom that parallel installation of qmake projects
            # does not work. So just use the usual make programs. It's hacky but
            # this was decided on the 2012 Windows sprint.
            if compiler.isMSVC() or compiler.isIntel():
                installmake="nmake /NOLOGO"
            elif compiler.isMinGW():
                installmake="mingw32-make"
        else:
            installmake = self.makeProgram

        if not self.subinfo.options.useShadowBuild:
            self.enterSourceDir()
        else:
            self.enterBuildDir()
        if options != None:
            command = "%s %s" % ( installmake, options )
        else:
            command = "%s install" % ( installmake )

        return self.system( command )


    def runTest( self ):
        """running qmake based unittests"""
        return True
    
    
    def configureOptions( self, defines=""):
        """returns default configure options"""
        defines += BuildSystemBase.configureOptions(self, defines)
        if self.buildType() == "Release" or self.buildType() == "RelWithDebInfo":
            defines += ' "CONFIG -= debug"'
            defines += ' "CONFIG += release"'
        elif self.buildType() == "Debug":
            defines += ' "CONFIG += debug"'
            defines += ' "CONFIG -= release"'
            
        return defines
        
    def ccacheOptions(self):
        return ' "QMAKE_CC=ccache gcc" "QMAKE_CXX=ccache g++" "CONFIG -= precompile_header" '
    
    def clangOptions(self):
        if OsUtils.isUnix():
            return ' "CONFIG -= precompile_header" '
        return ''
