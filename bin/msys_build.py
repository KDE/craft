# -*- coding: utf-8 -*-
# definitions for the msys build system
import os
import utils
import shells

class msys_interface:
    def __init__( self, env = dict( os.environ ) ):
        self.MSYSDIR = env[ "MSYSDIR" ]
        
    def setDirectories(self, rootdir, imagedir, workdir, instsrcdir, instdestdir):
        self.rootdir = rootdir
        self.imagedir = imagedir
        self.workdir = workdir
        self.instsrcdir = instsrcdir
        self.instdestdir = instdestdir
        self.msysdir = self.MSYSDIR
        self.msysCustomDefines = ""

    def __toMSysPath( self, path ):
        path = path.replace( '\\', '/' )
        if ( path[1] == ':' ):
            path = '/' + path[0].lower() + '/' + path[3:]
        return path

    def msysExecute( self, path, cmd, args ):
        sh = os.path.join( self.msysdir, "bin", "sh.exe" )

        cmd = "%s --login -c \"cd %s && %s %s" % \
              ( sh, self.__toMSysPath( path ), self.__toMSysPath( cmd ), args )

        cmd +="\""
        if utils.verbose() > 0:
            print "msys execute: %s" % cmd
        utils.system( cmd ) or utils.die( "msys execute failed. cmd: %s" % cmd )
        return True

    def msysConfigureFlags ( self ):
        """adding configure flags always used"""
        flags  = "--disable-nls "
        flags += "--enable-shared "
        flags += "--disable-static "
        flags += "--prefix=/ "
        flags += self.msysCustomDefines
        return flags

    def msysCompile( self, bOutOfSource = True ):
        """run configure and make for Autotools based stuff"""
        config = os.path.join( self.workdir, self.instsrcdir, "configure" )
        build  = os.path.join( self.workdir )
        if( bOutOfSource ):
           # otherwise $srcdir is very long and a conftest may fail (like it's the
           # case in libgmp-4.2.4)
           config = os.path.join( "..", self.instsrcdir, "configure" )
           build  = os.path.join( build, self.instsrcdir + "-build" )
           utils.cleanDirectory( build )
        else:
           build  = os.path.join( build, self.instsrcdir )

        sh = os.path.join( self.msysdir, "bin", "sh.exe" )

        # todo use msysexecute
        cmd = "%s --login -c \"cd %s && %s %s && make -j2" % \
              ( sh, self.__toMSysPath( build ), self.__toMSysPath( config ), \
                self.msysConfigureFlags() )
        if utils.verbose() > 1:
            cmd += " VERBOSE=1"
        cmd +="\""
        if utils.verbose() > 0:
            print "msys compile: %s" % cmd
        utils.system( cmd ) or utils.die( "msys compile failed. cmd: %s" % cmd )
        return True

    def msysInstall( self, bOutOfSource = True ):
        """run make install for Autotools based stuff"""
        install = os.path.join( self.imagedir, self.instdestdir )
        build  = os.path.join( self.workdir )
        if( bOutOfSource ):
           build  = os.path.join( build, self.instsrcdir + "-build" )
        else:
           build  = os.path.join( build, self.instsrcdir )

        sh = os.path.join( self.msysdir, "bin", "sh.exe" )

        # todo use msysexecute
        cmd = "%s --login -c \"cd %s && make -j2 install DESTDIR=%s\"" % \
              ( sh, self.__toMSysPath( build ), self.__toMSysPath( install ) )
        if utils.verbose() > 0:
            print "msys install: %s" % cmd
        utils.system( cmd ) or utils.die( "msys install failed. cmd: %s" % cmd )
        return True
