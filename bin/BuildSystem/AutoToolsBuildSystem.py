# -*- coding: utf-8 -*-
# definitions for the autotools build system

import os
import utils

from shells import *

from BuildSystem.BuildSystemBase import *

class AutoToolsBuildSystem(BuildSystemBase):
    def __init__( self ):
        self.buildInSource = False
        BuildSystemBase.__init__(self, "autotools")
        self.shell = MSysShell()
        self.makeProgram = "make -e"
        if self.subinfo.options.make.supportsMultijob:
            self.makeProgram += " -j%s" % os.getenv("NUMBER_OF_PROCESSORS")
        if emergePlatform.buildArchitecture() == "x86":
            self.platform = "--host=i686-w64-mingw32 --build=i686-w64-mingw32 --target=i686-w64-mingw32 "
        else:
            self.platform = "--host=x86_64-w64-mingw32 --build=x86_64-w64-mingw32 --target=x86_64-w64-mingw32 "


    def configureDefaultDefines( self ):

        """defining the default cmake cmd line"""
        return ""

    def configure( self, cflags="", ldflags=""):
        """configure the target"""
        with utils.LockFile(utils.LockFileName("MSYS")):
            if self.buildInSource:
                self.enterSourceDir()
            else:
                self.enterBuildDir()

            if self.noCopy:
                sourcedir = self.sourceDir()
            else:
                sourcedir = self.buildDir()



            configure = os.path.join(sourcedir, "configure")
            if os.path.exists(configure) or self.subinfo.options.configure.bootstrap == True:
                mergeroot = self.shell.toNativePath(self.mergeDestinationDir())
                self.shell.initEnvironment(cflags, ldflags)
                if self.subinfo.options.configure.bootstrap == True:
                    autogen = os.path.join(sourcedir, "autogen.sh")
                    if os.path.exists(autogen):
                        self.shell.execute(self.sourceDir(), autogen, debugLvl=0)
                #else:
                    #self.shell.execute(self.sourceDir(), "autoreconf -f -i", debugLvl=0)
                if self.subinfo.options.configure.noDefaultOptions == False:
                    if self.subinfo.options.install.useDestDir == False:
                        _prefix = "--prefix=" + self.shell.toNativePath(self.imageDir())
                    else:
                        _prefix = "--prefix=" + mergeroot
                else:
                    _prefix = ""
 
                _options = self.platform
                _options += BuildSystemBase.configureOptions(self)
                if _options:
                    _prefix += " %s" % _options
                if self.buildInSource:
                    ret = self.shell.execute(self.sourceDir(), configure, _prefix, debugLvl=0 )
                else:
                    ret = self.shell.execute(self.buildDir(), configure, _prefix, debugLvl=0  )
            else:
                ret = self.shell.execute(self.sourceDir(), "ruby", "configure", debugLvl=0 )
            return ret

    def make( self, dummyBuildType=None ):
        """Using the *make program"""
        with utils.LockFile(utils.LockFileName("MSYS")):
            if self.buildInSource:
                self.enterSourceDir()
            else:
                self.enterBuildDir()

            command = self.makeProgram
            args = self.makeOptions()

            # adding Targets later
            if self.buildInSource:
                if not self.shell.execute(self.sourceDir(), self.makeProgram , "clean"):
                    utils.die( "while Make'ing. cmd: %s clean" % self.makeProgram)
                if not self.shell.execute(self.sourceDir(), command, args ):
                    utils.die( "while Make'ing. cmd: %s" % command )
            else:
                if not self.shell.execute(self.buildDir(), command, args ):
                    utils.die( "while Make'ing. cmd: %s" % command )
            return True

    def install( self ):
        """Using *make install"""

        with utils.LockFile(utils.LockFileName("MSYS")):
            if self.buildInSource:
                self.enterSourceDir()
            else:
                self.enterBuildDir()

            command = self.makeProgram
            args = "install"

            if self.subinfo.options.install.useDestDir == True:
                args += " DESTDIR=%s prefix=" % self.shell.toNativePath( self.installDir() )

            if self.subinfo.options.make.ignoreErrors:
                args += " -i"

            if self.subinfo.options.make.makeOptions:
                args += " %s" % self.subinfo.options.make.makeOptions
            if self.buildInSource:
                self.shell.execute(self.sourceDir(), command, args) or utils.die( "while installing. cmd: %s %s" % (command, args) )
            else:
                self.shell.execute(self.buildDir(), command, args) or utils.die( "while installing. cmd: %s %s" % (command, args) )
            if os.path.exists(os.path.join(self.imageDir(),"lib")):
                return self.shell.execute(os.path.join(self.imageDir(),"lib"), "rm", " -Rf *.la")
            else:
                return True

    def runTest( self ):
        """running unittests"""
        return True

