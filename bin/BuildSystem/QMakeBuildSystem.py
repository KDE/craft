#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# definitions for the qmake build system

import os
import utils

from BuildSystem.BuildSystemBase import *

class QMakeBuildSystem(BuildSystemBase):
    def __init__( self):
        BuildSystemBase.__init__(self, "qmake")
        self.platform = ""
        if self.compiler() == "msvc2005" or self.compiler() == "msvc2008" or self.compiler() == "msvc2010":
            self.platform = "win32-%s" % self.compiler()
        elif self.compiler() == "mingw" or self.compiler() == "mingw4":
            self.platform = "win32-g++"
        else:
            exit( 1 )

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
        elif os.path.exists(qmakeTool) and os.path.exists(topLevelProFile) and topLevelProFilesFound == 1:
            command = "qmake -makefile %s %s" % (topLevelProFile, self.configureOptions(configureDefines))
        elif os.path.exists(qmakeTool):
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

        self.enterBuildDir()
        if options != None:
            command = "%s %s" % ( self.makeProgramm, options )
        else:
            command = "%s install" % ( self.makeProgramm )

        return self.system( command )

    def runTest( self ):
        """running qmake based unittests"""
        return True
