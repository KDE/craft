# -*- coding: utf-8 -*-
# definitions for the autotools build system

import os
import utils

import base
import info
from shells import *

from BuildSystemBase import *

class AutoToolsBuildSystem(BuildSystemBase):
    def __init__( self ):
        BuildSystemBase.__init__(self,"autotools")
        self.shell = MSysShell()
        self.makeProgram = "mingw32-make"
            
    def configureDefaultDefines( self ):
        """defining the default cmake cmd line"""
        return ""

    def configure( self, cflags="", ldflags=""):
        """configure the target"""
            
        self.enterBuildDir()

        if self.noCopy:
            sourcedir = self.sourceDir()
        else: 
            sourcedir = self.buildDir()
        
        configure = os.path.join(sourcedir,"configure")
        if os.path.exists(configure):
            mergeroot = self.mergeDestinationDir().replace('\\','/') 
            _cflags = "-I%s/include %s" % (mergeroot, cflags)
            _ldflags = "-L%s/lib %s" % (mergeroot, ldflags)
            utils.putenv("CFLAGS",_cflags)
            utils.putenv("LDFLAGS",_ldflags)
            ret = self.shell.execute(self.buildDir(), configure, "" )
        else:
            ret = self.shell.execute(self.sourceDir(), "ruby configure", "" )
        return ret

    def make( self, buildType=None ):
        """Using the *make program"""

        self.enterBuildDir()
        
        command = self.makeProgram
        args = "-j2"
        if self.subinfo.options.make.ignoreErrors:
            args += " -i"
            
        if self.subinfo.options.make.makeOptions:
            args += " %s" % self.subinfo.options.make.makeOptions
        
        # adding Targets later
        if utils.verbose() > 1:
            args += " VERBOSE=1"
        self.shell.execute(self.buildDir(), command, args ) or utils.die( "while Make'ing. cmd: %s" % command )
        return True

    def install( self ):
        """Using *make install"""

        self.enterBuildDir()
        args = "prefix= DESTDIR=%s install" % self.shell.toNativePath(self.installDir())             

        if self.subinfo.options.make.ignoreErrors:
            args += " -i"
            
        if self.subinfo.options.make.makeOptions:
            args += " %s" % self.subinfo.options.make.makeOptions
        
        return self.shell.execute(self.buildDir(), self.makeProgram, args ) or utils.die( "while installing. cmd: %s" % command )

    def runTest( self ):
        """running unittests"""
        return true
        
    def createShell( self ):
        """create shell in package build dir with prepared environment"""

        self.enterBuildDir()
        self.shell.openShell(self.buildDir())
        return True
        