#!/usr/bin/env python

"""
    provides shells
"""

import os
import sys

from CraftDebug import craftDebug
import utils
from CraftCompiler import craftCompiler
from options import *


## \todo requires installed msys package -> add suport for installing packages

class MSysShell(object):
    def __init__(self):
        self.msysdir = os.path.join( CraftStandardDirs.msysDir())
        self.environment = {}
        self._sh = os.path.join( self.msysdir, "bin", "sh.exe" )
        if not os.path.exists( self._sh ):
            self._sh = os.path.join( self.msysdir, "usr", "bin", "bash.exe" )

        mergeroot = self.toNativePath(CraftStandardDirs.craftRoot())
        if craftCompiler.isMSVC():
            ldflags = ""
            cflags = " -O2 -MD -GR -W3 -EHsc -D_USE_MATH_DEFINES -DWIN32_LEAN_AND_MEAN -DNOMINMAX -D_CRT_SECURE_NO_WARNINGS"  # dynamic and exceptions enabled
            if craftCompiler.getMsvcPlatformToolset() > 120:
                cflags += " -FS"
        else:
            ldflags = "-L%s/lib " % mergeroot
            cflags = "-I%s/include " % mergeroot

            if self.buildType == "RelWithDebInfo":
                cflags += " -O2 -g "
            elif self.buildType == "Debug":
                cflags += " -O0 -g3 "


        self.environment[ "MSYS2_PATH_TYPE" ] = "inherit"#inherit the windows path
        self.environment[ "PKG_CONFIG_PATH" ] = self.toNativePath(os.path.join( CraftStandardDirs.craftRoot( ), "lib", "pkgconfig" ))

        if "make" in self.environment:
            del self.environment[ "make" ]
        arch = "32"
        if craftCompiler.isX64():
            arch = "64"
        if craftCompiler.isMinGW():
            self.environment[ "MSYSTEM" ] = f"MINGW{arch}_CRAFT"
        elif craftCompiler.isMSVC():
            self.environment["MSYSTEM"] = f"CYGWIN{arch}_CRAFT"
        self.environment[ "CFLAGS" ] = cflags
        self.environment[ "CXXFLAGS" ] = cflags
        self.environment[ "LDFLAGS" ] = ldflags

        if craftCompiler.isMSVC():
            if False:
                cl = "clang-cl"
            else:
                cl = "cl"
            self.environment[ "LIB" ] = f"{os.environ['LIB']};{CraftStandardDirs.craftRoot()}\\lib"
            self.environment[ "INCLUDE" ] = f"{os.environ['INCLUDE']};{CraftStandardDirs.craftRoot()}\\include"
            self.environment[ "LD" ] = "link -NOLOGO"
            self.environment[ "CC" ] = "%s -nologo" % cl
            self.environment[ "CXX" ] = self.environment[ "CC" ]
            self.environment[ "CPP"] = "%s -nologo -EP" %cl
            self.environment[ "CXXCPP"] = self.environment[ "CPP"]
            self.environment[ "NM" ] = "dumpbin -symbols"
            self.environment[ "AR" ] = "lib"
            self.environment[ "WINDRES"] = "rc"
            #self.environment[ "RC","rc-windres"
            self.environment[ "STRIP"] = ":"
            self.environment[ "RANLIB"] = ":"
            self.environment[ "F77" ] = "no"
            self.environment[ "FC" ] = "no"


    @property
    def buildType(self):
        return craftSettings.get("Compile", "BuildType","RelWithDebInfo")

    @staticmethod
    def toNativePath( path ):
        return utils.toMSysPath( path )

    def execute(self, path, cmd, args="", out=sys.stdout, err=sys.stderr, displayProgress=False):
        export = ""
        env = os.environ.copy()
        for k,v in self.environment.items():
            export += "%s='%s' " % (k, v)
            env[k] = v
        command = "%s --login -c \"export %s &&cd %s && %s %s\"" % \
                  ( self._sh, export, self.toNativePath( path ), self.toNativePath( cmd ), args )
        craftDebug.step("msys execute: %s" % command)
        craftDebug.log.debug("msys environment: %s" % self.environment)
        return utils.system( command, stdout=out, stderr=err, env = env, displayProgress=displayProgress )

    def login(self):
        self.environment[ "CHERE_INVOKING" ] = "1"
        command = "bash --login -i"
        return self.execute(".", command, displayProgress=True)


def main():
    shell = MSysShell()
    shell.login()

if __name__ == '__main__':
    main()
