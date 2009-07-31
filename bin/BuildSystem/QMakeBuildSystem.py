# -*- coding: utf-8 -*-
# definitions for the qmake build system

import os
import utils

import base
import info

from BuildSystemBase import *

class QMakeBuildSystem(BuildSystemBase):
    def __init__( self, configureOptions="", makeOptions=""):
        BuildSystemBase.__init__(self,"qmake",configureOptions,makeOptions)
        
    def configure( self, buildType=None, customOptions="" ):
        """Using qmake"""
            
        self.enterBuildDir()
        
        # so that the mkspecs can be found, when -prefix is set
        os.putenv( "QMAKEPATH", self.sourceDir() )

        # here follows some automatic configure tool detection
        # 1. search for configure.exe 
        # 2. search for a pro-file named as the package 
        # 3. if a pro-file is available through configureOptions, run it with qmake
        # 4. if a complete configure command line is available run it 
        configTool = os.path.join(self.sourceDir(),"configure.exe")
        topLevelProFile = os.path.join(self.sourceDir(),self.package + ".pro")
        if os.path.exists(configTool):
            command = configTool + " " + self.configureOptions()
        elif os.path.exists(topLevelProFile):
            command = "qmake " + topLevelProFile
        elif self.configureOptions() != "":
            command = "qmake " + self.configureOptions()
        elif self.configureTool() != "":
            command = self.configureTool()
        else:
            utils.die("could not find configure.exe or top level pro-file, please take a look into the source and setup the config process.")

        if utils.verbose() > 0:
            print "configuration command: %s" % command
        utils.system( command ) or utils.die( "while CMake'ing. cmd: %s" % command )
        return True

    def makeOptions(self):
        return ""

    def make( self, buildType=None ):
        """Using the make program"""

        self.enterBuildDir()

        # so that the mkspecs can be found, when -prefix is set
        os.putenv( "QMAKEPATH", self.sourceDir() )

        command = self.cmakeMakeProgramm 
        #if self.makeOptions() <> "": 
        #    command += " " + self.makeOptions()
        # adding Targets later
        if utils.verbose() > 1:
            command += " VERBOSE=1"
        utils.system( command ) or utils.die( "while Make'ing. cmd: %s" % command )
        return True

    def __install( self, buildType=None ):
        """Using *make install"""

        self.enterBuildDir()
        command = "%s DESTDIR=%s install" % ( self.cmakeMakeProgramm, self.installDir() )
        
        utils.system( command ) or utils.die( "while installing. cmd: %s" % command )
        return True

    def install( self ):
        """making all required stuff for installing qmake based modules"""
        if( not self.buildType() == None ):
            if( not self.__install( self.buildType() ) ):
                return False
        else:
            if( not self.__install( "debug" ) ):
                return False
            if( not self.__install( "release" ) ):
                return False
        return True

    def runTest( self ):
        """running qmake based unittests"""
        return True
