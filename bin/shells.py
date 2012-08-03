#!/usr/bin/env python

"""
    provides shells
"""

import os
import utils
import sys
import compiler

## \todo requires installed msys package -> add suport for installing packages

class MSysShell(object):
    def __init__(self):
        self.msysdir = os.path.join( os.environ.get( "KDEROOT" ), "msys" )
        self.buildType = os.getenv("EMERGE_BUILDTYPE")
        self.initEnvironment()


    def initEnvironment(self, cflags="", ldflags=""):
        mergeroot = self.toNativePath(os.getenv("KDEROOT"))
        cflags = "-I%s/include %s" % (mergeroot, cflags)
        ldflags = "-L%s/lib %s" % (mergeroot, ldflags)
        if compiler.isMinGW():
            if self.buildType == "RelWithDebInfo":
                cflags += " -O2 -g "
            elif self.buildType == "Debug":
                cflags += " -O0 -g3 "
        elif compiler.isMSVC():
            utils.putenv("LD", "link.exe")

        utils.putenv("CFLAGS", cflags)
        utils.putenv("LDFLAGS", ldflags)
        #unset make to remove things like jom
        if "MAKE" in os.environ:
            del os.environ["MAKE"]
        utils.putenv("PATH", "%s;%s" %  ( os.environ.get( "PATH" ), os.path.join( os.environ.get( "KDEROOT" ), "dev-utils", "bin" )))
        #seting perl to prevent msys from using msys-perl
        perl = self.toNativePath(os.path.join( os.environ.get( "KDEROOT" ), "dev-utils", "bin", "perl.exe" ))
        utils.putenv("PERL", perl)
        utils.putenv("INTLTOOL_PERL", perl)

        #prepare path to sue autotools
        utils.putenv("PATH", "%s;%s" %  ( os.environ.get( "PATH" ), os.path.join( self.msysdir, "opt", "autotools", "bin" )))


    def toNativePath( self, path ):
        path = path.replace( '\\', '/' )
        if ( path[1] == ':' ):
            path = '/' + path[0].lower() + '/' + path[3:]
        return path

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
    shell.initEnvironment()
    utils.putenv("MSYS_LOGIN_DIR",os.getcwd())
    utils.system("%s %s" % (os.path.join( shell.msysdir, "bin", "sh.exe" ), "--login -i"))

if __name__ == '__main__':
    main()
