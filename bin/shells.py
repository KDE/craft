#!/usr/bin/env python

"""
    provides shells     
"""

import os
import utils
import sys

## \todo requires installed msys package -> add suport for installing packages 

class Shell(object):
    def __init__(self):
        dummy = 0

    #""" convert internal used paths to native path which are understandable by the shell
    def toNativePath( self, path ): abstract

    #""" execute shell command
    def execute(self, path, cmd, args): abstract
    

class MSysShell(Shell):
    def __init__(self):
        Shell.__init__(self)
        env = dict( os.environ )
        self.msysdir = env[ "MSYSDIR" ]

    def toNativePath( self, path ):
        path = path.replace( '\\', '/' )
        if ( path[1] == ':' ):
            path = '/' + path[0].lower() + '/' + path[3:]
        return path

    def execute( self, path, cmd, args, out=sys.stdout, err=sys.stderr ):
        sh = os.path.join( self.msysdir, "bin", "sh.exe" )

        cmd = "%s --login -c \"cd %s && %s %s" % \
              ( sh, self.toNativePath( path ), self.toNativePath( cmd ), args )

        cmd +="\""
        if utils.verbose() > 0:
            print "msys execute: %s" % cmd
        return utils.system( cmd, outstream=out, errstream=err )
