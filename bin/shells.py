#!/usr/bin/env python

"""
    provides shells
"""

import os
import sys

import utils
import compiler
from options import *


## \todo requires installed msys package -> add suport for installing packages

class MSysShell(object):
    def __init__(self):
        self.msysdir = os.path.join( EmergeStandardDirs.emergeRoot(), "msys" )
        self.environment = dict()
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
            cflags = " -MD -Zi"
            if compiler.isMSVC2013():
                cflags = " -FS"

        self.environment[ "CFLAGS" ] = cflags
        self.environment[ "CXXFLAGS" ] = cflags
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
        return emergeSettings.get("General", "EMERGE_BUILDTYPE","RelWithDebInfo")


    def _environmentSetup(self):
        # unset make to remove things like jom
        #this cant be set using export
        utils.putenv("MAKE", "")
        out = ""
        for var, val in  self.environment.items():
            out += "%s='%s' " %( var, val )
        return out


    @staticmethod
    def toNativePath( path ):
        return utils.toMSysPath( path )

    def execute( self, path, cmd, args = "", out=sys.stdout, err=sys.stderr, debugLvl=1 ):
        command = "%s --login -c \"export %s && cd %s && %s %s\"" % \
                  ( self._sh, self._environmentSetup(), self.toNativePath( path ), self.toNativePath( cmd ), args )
        if debugLvl == 0:
            print("%s %s" % (cmd, args))
        else:
            utils.debug( "msys execute: %s" % command, debugLvl )
        return utils.system( command, stdout=out, stderr=err )

    def login(self):
        self.environment[ "CHERE_INVOKING" ] = "1"
        command = "bash --login -i"
        return self.execute( ".", command )


def main():
    shell = MSysShell()
    shell.login()

if __name__ == '__main__':
    main()
