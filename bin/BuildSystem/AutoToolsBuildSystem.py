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
            
        if self.buildInSource:
            self.enterSourceDir()
        else:
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
            _prefix = "--prefix=" + mergeroot
            if self.buildInSource:
                ret = self.shell.execute(self.sourceDir(), configure, _prefix )
            else:
                ret = self.shell.execute(self.buildDir(), configure, _prefix )
        else:
            ret = self.shell.execute(self.sourceDir(), "ruby configure", "" )
        return ret

    def make( self, buildType=None ):
        """Using the *make program"""

        if self.buildInSource:
            self.enterSourceDir()
        else:
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
        if self.buildInSource:
            self.shell.execute(self.sourceDir(), command, args ) or utils.die( "while Make'ing. cmd: %s" % command )
        else:
            self.shell.execute(self.buildDir(), command, args ) or utils.die( "while Make'ing. cmd: %s" % command )
        return True

    def install( self ):
        """Using *make install"""

        if self.buildInSource:
            self.enterSourceDir()
        else:
            self.enterBuildDir()
        args = "prefix= DESTDIR=%s install" % self.shell.toNativePath(self.installDir())             

        if self.subinfo.options.make.ignoreErrors:
            args += " -i"
            
        if self.subinfo.options.make.makeOptions:
            args += " %s" % self.subinfo.options.make.makeOptions
        if self.buildInSource:
            return self.shell.execute(self.sourceDir(), self.makeProgram, args ) or utils.die( "while installing. cmd: %s" % command )
        else:
            return self.shell.execute(self.buildDir(), self.makeProgram, args ) or utils.die( "while installing. cmd: %s" % command )

    def runTest( self ):
        """running unittests"""
        return true
        
    def createShell( self ):
        """create shell in package build dir with prepared environment"""

        if self.buildInSource:
            self.enterSourceDir()
            self.shell.openShell(self.sourceDir())
        else:
            self.enterBuildDir()
            self.shell.openShell(self.buildDir())
        return True
        