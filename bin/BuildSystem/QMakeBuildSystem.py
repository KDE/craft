#
# copyright (c) 2009 Ralf Habacker <ralf.habacker@freenet.de>
#
# definitions for the qmake build system

import utils
import compiler

from BuildSystem.BuildSystemBase import *

class QMakeBuildSystem(BuildSystemBase):
    def __init__( self ):
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


    def configure( self, configureDefines="" ):
        """inplements configure step for Qt projects"""
        self.enterBuildDir()
        if self.buildType() == "Release" or self.buildType() == "RelWithDebInfo":
            configureDefines += ' "CONFIG -= debug"'
            configureDefines += ' "CONFIG += release"'
        elif self.buildType() == "Debug":
            configureDefines += ' "CONFIG += debug"'
            configureDefines += ' "CONFIG -= release"'

        
        command = "qmake -makefile %s %s" % (self.configureSourceDir(), self.configureOptions(configureDefines))

        return self.system( command, "configure" )

    def make( self, options=""):
        """implements the make step for Qt projects"""
        self.enterBuildDir()
        
        command = ' '.join([self.makeProgramm, self.makeOptions(options, maybeVerbose=False)])

        return self.system( command, "make" )

    def install( self, options=None ):
        """implements the make step for Qt projects"""
        if not BuildSystemBase.install(self):
            return False

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
        
    def ccacheOptions(self):
        return ' "QMAKE_CC=ccache gcc" "QMAKE_CXX=ccache g++" "CONFIG -= precompile_header" '
