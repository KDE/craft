# 
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# definitions for the qmake build system

import os
import utils

import base
import info
import compilercache
from BuildSystemBase import *

class QMakeBuildSystem(BuildSystemBase):
    def __init__( self):
        BuildSystemBase.__init__(self,"qmake","QMakeBuildSystem")
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
        utils.putenv( "QMAKESPEC", os.path.join(self.sourceDir(),'mkspecs',self.platform ))

    def configure( self, configureTool=None, configureDefines="" ):
        """inplements configure step for Qt projects"""
            
        self.enterBuildDir()

        # here follows some automatic configure tool detection
        # 1. search for configure.exe in the order 
        #      a. provided by method call 
        #      b. in source dir 
        # 2. if qmake is available search for a pro-file named as the package 
        # 3. if a pro-file is available through configureOptions, run it with qmake
        # 4. otherwise run qmake without any pro file given 
        configTool = os.path.join(self.sourceDir(),"configure.exe")
        qmakeTool = os.path.join(self.mergeDestinationDir(),"bin","qmake.exe")
        topLevelProFile = self.sourceDir()
        if configureTool != None:
            command = "%s %s" % (configureTool, self.configureOptions(configureDefines))
        elif os.path.exists(configTool):
            command = "%s %s" % (configTool, self.configureOptions(configureDefines))
        elif os.path.exists(qmakeTool) and os.path.exists(topLevelProFile):
            command = "qmake -makefile %s" % (topLevelProFile) # , self.configureOptions(configureDefines)
        elif os.path.exists(qmakeTool):
            command = "qmake %s" % self.configureOptions(configureDefines)
        else:
            utils.die("could not find configure.exe or top level pro-file, please take a look into the source and setup the config process.")

        return self.system( command, "configure" )

    def make( self, options=""):
        """implements the make step for Qt projects"""
        self.enterBuildDir()

        command = self.makeProgramm 
        command += compilercache.getQmakeMakeArguments()
        
        if utils.verbose() > 1:
            command += " VERBOSE=1"
            
        command += " %s" % self.makeOptions(options)
            
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
