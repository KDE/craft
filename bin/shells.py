#!/usr/bin/env python

"""
    provides shells     
"""

class Shell(object):
    def __init__(self):
        dummy = 0

    #""" convert internal used paths to native path which are understandable by the shell
    def toNativePath( self, path ): abstract

    #""" execute shell command
    def execute(self, path, cmd, args): abstract
    

class MSysShell(Shell):
    def __init__(self):
        Shell.__init(self)

    def toNativePath( self, path ):
        path = path.replace( '\\', '/' )
        if ( path[1] == ':' ):
            path = '/' + path[0].lower() + '/' + path[3:]
        return path

    def execute( self, path, cmd, args ):
        sh = os.path.join( self.msysdir, "bin", "sh.exe" )

        cmd = "%s --login -c \"cd %s && %s %s" % \
              ( sh, self.__toMSysPath( path ), self.__toMSysPath( cmd ), args )

        cmd +="\""
        if utils.verbose() > 0:
            print "msys execute: %s" % cmd
        utils.system( cmd ) or utils.die( "msys execute failed. cmd: %s" % cmd )
        return True
