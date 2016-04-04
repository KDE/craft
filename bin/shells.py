#!/usr/bin/env python

"""
    provides shells
"""

import os
import sys

import EmergeDebug
import utils
import compiler
from options import *


## \todo requires installed msys package -> add suport for installing packages

class MSysShell(object):
    def __init__(self):
        self.msysdir = os.path.join( EmergeStandardDirs.emergeRoot(), "msys" )
        self.environment = os.environ.copy()
        self._sh = os.path.join( self.msysdir, "bin", "sh.exe" )
        if not os.path.exists( self._sh ):
            self._sh = os.path.join( self.msysdir, "usr", "bin", "bash.exe" )

        mergeroot = self.toNativePath(EmergeStandardDirs.emergeRoot())
        if compiler.isMinGW():
            ldflags = "-L%s/lib " % mergeroot
            cflags = "-I%s/include " % mergeroot

            if self.buildType == "RelWithDebInfo":
                cflags += " -O2 -g "
            elif self.buildType == "Debug":
                cflags += " -O0 -g3 "
        elif compiler.isMSVC():
            ldflags = ""
            cflags = " -MD -Zi"
            if compiler.isMSVC2013():
                cflags = " -FS"

        self.environment[ "SET_FULL_PATH" ] = "1"#inherit the windows path
        if "make" in self.environment:
            del self.environment[ "make" ]
        if compiler.isMinGW():
            arch = "32"
            if compiler.isX64():
                arch = "64"
            self.environment[ "MSYSTEM" ] = "MINGW%s_EMERGE" % arch
        self.environment[ "CFLAGS" ] = cflags
        self.environment[ "CXXFLAGS" ] = cflags

        if ldflags != "":
            self.environment[ "LDFLAGS" ] = ldflags


        if compiler.isMSVC():
            self.environment[ "LIB" ] = "%s;%s\\lib" % ( os.getenv("LIB"), EmergeStandardDirs.emergeRoot())
            self.environment[ "INCLUDE" ] = "%s;%s\\include" % ( os.getenv("INCLUDE"), EmergeStandardDirs.emergeRoot())
            self.environment[ "LD" ] = "link"
            self.environment[ "CC" ] = "cl -nologo"
            self.environment[ "CXX" ] = "cl -nologo"
            self.environment[ "NM" ] = "dumpbin -symbols"
            self.environment[ "AR" ] = "lib"
            #self.environment[ "WINDRES","rc-windres"
            #self.environment[ "RC","rc-windres"
            self.environment[ "STRIP"] = ":"
            self.environment[ "RANLIB"] = ":"
            self.environment[ "F77" ] = "no"
            self.environment[ "FC" ] = "no"


    @property
    def buildType(self):
        return emergeSettings.get("Compile", "BuildType","RelWithDebInfo")

    @staticmethod
    def toNativePath( path ):
        return utils.toMSysPath( path )

    def execute(self, path, cmd, args="", out=sys.stdout, err=sys.stderr):
        command = "%s --login -c \"cd %s && %s %s\"" % \
                  ( self._sh, self.toNativePath( path ), self.toNativePath( cmd ), args )
        EmergeDebug.info("msys execute: %s" % command)
        EmergeDebug.debug("msys environment: %s" % self.environment)
        return utils.system( command, stdout=out, stderr=err , env=self.environment)

    def login(self):
        self.environment[ "CHERE_INVOKING" ] = "1"
        command = "bash --login -i"
        return self.execute(".", command)


def main():
    shell = MSysShell()
    shell.login()

if __name__ == '__main__':
    main()
