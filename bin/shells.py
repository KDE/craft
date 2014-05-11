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
        self.envirnmentIsSetup = False

    @property
    def buildType(self):
        return emergeSettings.get("General", "EMERGE_BUILDTYPE","RelWithDebInfo")

    def initEnvironment(self, cflags="", ldflags=""):

        mergeroot = self.toNativePath(EmergeStandardDirs.emergeRoot())
        if compiler.isMinGW():
            ldflags = "-L%s/lib %s" % (mergeroot, ldflags)
            cflags = "-I%s/include %s" % (mergeroot, cflags)

            if self.buildType == "RelWithDebInfo":
                cflags += " -O2 -g "
            elif self.buildType == "Debug":
                cflags += " -O0 -g3 "
        elif compiler.isMSVC():
            cflags += " -MD -Zi"
            if compiler.isMSVC2013():
                cflags += " -FS"

        utils.putenv("CFLAGS", cflags)
        utils.putenv("LDFLAGS", ldflags)


        if self.envirnmentIsSetup:
            return
        self.envirnmentIsSetup = True


        if compiler.isMSVC():
            utils.putenv("LIB", "%s;%s\\lib" % ( os.getenv("LIB"), EmergeStandardDirs.emergeRoot()))
            utils.putenv("INCLUDE", "%s;%s\\include" % ( os.getenv("INCLUDE"), EmergeStandardDirs.emergeRoot()))
            utils.putenv("LD", "link")
            utils.putenv("CC", "cl -nologo")
            utils.putenv("CXX", "cl -nologo")
            utils.putenv("NM", "dumpbin -symbols")
            utils.putenv("AR", "lib")
            #utils.putenv("WINDRES","rc-windres")
            #utils.putenv("RC","rc-windres")
            utils.putenv("STRIP",":")
            utils.putenv("RANLIB",":")
            utils.putenv("F77", "no")
            utils.putenv("FC", "no")

        #unset make to remove things like jom
        if "MAKE" in os.environ:
            del os.environ["MAKE"]



    @staticmethod
    def toNativePath( path ):
        return utils.toMSysPath( path )

    def execute( self, path, cmd, args = "", out=sys.stdout, err=sys.stderr, debugLvl=1 ):
        self.initEnvironment()
        sh = os.path.join( self.msysdir, "bin", "sh.exe" )

        command = "%s --login -c \"cd %s && %s %s" % \
              ( sh, self.toNativePath( path ), self.toNativePath( cmd ), args )

        command += "\""
        if debugLvl == 0:
            print("%s %s" % (cmd, args))
        else:
            utils.debug( "msys execute: %s" % command, debugLvl )
        return utils.system( command, stdout=out, stderr=err )

def main():
    shell = MSysShell()
    utils.putenv("CHERE_INVOKING","1")
    utils.system("%s %s" % (os.path.join( shell.msysdir, "bin", "sh.exe" ), "--login -i"))

if __name__ == '__main__':
    main()
