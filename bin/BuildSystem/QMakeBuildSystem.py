#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# definitions for the qmake build system

import os
import utils
import compiler

from BuildSystem.BuildSystemBase import *

class QMakeBuildSystem(BuildSystemBase):
    def __init__( self):
        BuildSystemBase.__init__(self, "qmake")
        self.platform = ""
        if compiler.isMSVC():
            self.platform = "win32-%s" % self.compiler()
        elif compiler.isMinGW():
            self.platform = "win32-g++"
        elif compiler.isIntel():
            self.platform = "win32-icc"
        else:
            utils.die( "QMakeBuildSystem: unsupported compiler platform %s" % self.compiler() )

    def setPathes( self ):
            # for building qt with qmake
        utils.putenv( "PATH", os.path.join( self.buildDir(), "bin" ) + ";" + os.getenv("PATH") )

        # so that the mkspecs can be found, when -prefix is set
        utils.putenv( "QMAKEPATH", self.sourceDir() )
        # to be sure
        utils.putenv( "QMAKESPEC", os.path.join(self.sourceDir(), 'mkspecs', self.platform ))

    def configure( self, configureDefines="" ):
        """inplements configure step for Qt projects"""

        self.enterBuildDir()

        # here follows some automatic configure tool detection
        # 1. search for configure.exe in the order
        #      a. provided by method call
        #      b. in source directory
        # 2. if qmake is available search for a pro-file named as the package
        # 3. if a pro-file is available through configureOptions, run it with qmake
        # 4. otherwise run qmake without any pro file given
        configTool = os.path.join(self.configureSourceDir(), "configure.exe")
        qmakeTool = os.path.join(self.mergeDestinationDir(), "bin", "qmake.exe")
        topLevelProFilesFound = 0
        topLevelProFile = ""
        for fileListed in os.listdir(self.configureSourceDir()):
            if fileListed.endswith(".pro"):
                if topLevelProFilesFound == 0:
                    topLevelProFile = os.path.join(self.configureSourceDir(), fileListed)
                topLevelProFilesFound += 1
        if self.subinfo.options.configure.tool != None and self.subinfo.options.configure.tool != False:
            command = "%s %s" % (self.subinfo.options.configure.tool, self.configureOptions(configureDefines))
        elif os.path.exists(configTool):
            command = "%s %s" % (configTool, self.configureOptions(configureDefines))
        elif os.path.exists(qmakeTool):
            if utils.envAsBool("EMERGE_USE_CCACHE") and compiler.isMinGW():
                configureDefines += ' "QMAKE_CC=ccache gcc" "QMAKE_CXX=ccache g++" '
            if self.buildType() == "Release":
                configureDefines += ' "CONFIG -= debug"'
                configureDefines += ' "CONFIG += release"'
                configureDefines += ' "CONFIG -= debug_and_release"'
            elif self.buildType() == "Debug":
                configureDefines += ' "CONFIG += debug"'
                configureDefines += ' "CONFIG -= release"'
                configureDefines += ' "CONFIG -= debug_and_release"'
            elif self.buildType() == "RelWithDebInfo":
                configureDefines += ' "CONFIG -= debug"'
                configureDefines += ' "CONFIG -= release"'
                configureDefines += ' "CONFIG += debug_and_release"'
            if os.path.exists(topLevelProFile) and topLevelProFilesFound == 1:
                command = "qmake -makefile %s %s" % (topLevelProFile, self.configureOptions(configureDefines))
            else:
                command = "qmake %s" % self.configureOptions(configureDefines)
        else:
            utils.die("could not find configure.exe or top level pro-file, please take a look into the source and setup the config process.")

        return self.system( command, "configure" )

    def make( self, options=""):
        """implements the make step for Qt projects"""
        self.enterBuildDir()

        command = ' '.join([self.makeProgramm, self.makeOptions(options, maybeVerbose=False)])

        return self.system( command, "make" )

    def install( self, options=None ):
        """implements the make step for Qt projects"""

        # There is a bug in jom that parallel installation of qmake projects
        # does not work. So just use the usual make programs. It's hacky but
        # this was decided on the 2012 Windows sprint.
        if compiler.isMSVC() or compiler.isIntel():
            installmake="nmake /NOLOGO"
        elif compiler.isMinGW():
            installmake="mingw32-make"

        self.enterBuildDir()
        if options != None:
            command = "%s %s" % ( installmake, options )
        else:
            command = "%s install" % ( installmake )

        return self.system( command )

    def runTest( self ):
        """running qmake based unittests"""
        return True
