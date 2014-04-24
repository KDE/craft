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
        self.msysdir = os.path.join( emergeRoot(), "msys" )
        self.buildType = emergeSettings.args.buildType
        self.options = Options()
        self.options.readFromEnv()
        self.initEnvironment()


    def initEnvironment(self, cflags="", ldflags=""):
        mergeroot = self.toNativePath(emergeRoot())

        if compiler.isMinGW():
            ldflags = "-L%s/lib %s" % (mergeroot, ldflags)
            cflags = "-I%s/include %s" % (mergeroot, cflags)
            if self.buildType == "RelWithDebInfo":
                cflags += " -O2 -g "
            elif self.buildType == "Debug":
                cflags += " -O0 -g3 "
        elif compiler.isMSVC():
            utils.putenv("LIB", "%s;%s\\lib" % ( os.getenv("LIB"), emergeRoot()))
            utils.putenv("INCLUDE", "%s;%s\\include" % ( os.getenv("INCLUDE"), emergeRoot()))
            utils.putenv("LD", "link")
            utils.putenv("CC", "/share/automake-1.13/compile cl -nologo")
            utils.putenv("CXX", "/share/automake-1.13/compile cl -nologo")
            utils.putenv("NM", "dumpbin -symbols")
            utils.putenv("AR", "/share/automake-1.13/ar-lib lib")
            utils.putenv("WINDRES","rc-windres")
            utils.putenv("RC","rc-windres")
            utils.putenv("STRIP",":")
            utils.putenv("RANLIB",":")
            utils.putenv("F77", "no")
            utils.putenv("FC", "no")
            cflags += " -MD -Zi"

        
        utils.putenv("PKG_CONFIG_PATH", "%s/lib/pkgconfig" % mergeroot)

        utils.putenv("CFLAGS", cflags)
        utils.putenv("LDFLAGS", ldflags)
        #unset make to remove things like jom
        if "MAKE" in os.environ:
            del os.environ["MAKE"]
        utils.putenv("PATH", "%s;%s" %  ( os.environ.get( "PATH" ), os.path.join( emergeRoot(), "dev-utils", "bin" )))
        if not self.options.features.msys2:
            #seting perl to prevent msys from using msys-perl
            perl = self.toNativePath(os.path.join( emergeRoot(), "dev-utils", "bin", "perl.exe" ))
            utils.putenv("PERL", perl)
            utils.putenv("INTLTOOL_PERL", perl)

            #prepare path to use autotools
            utils.putenv("PATH", "%s;%s" %  ( os.environ.get( "PATH" ), os.path.join( self.msysdir, "opt", "autotools", "bin" )))
        else:
            utils.putenv("MSYSTEM","MINGW32")


    def toNativePath( self, path ):
        return utils.toMSysPath( path )

    def execute( self, path, cmd, args = "", out=sys.stdout, err=sys.stderr, debugLvl=1 ):
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
