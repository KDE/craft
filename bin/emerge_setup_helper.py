# -*- coding: utf-8 -*-
# Helper script for substitution of paths, independent of cmd or powershell
# copyright:
# Patrick von Reth <vonreth [AT] kde [DOT] org>

import subprocess
import argparse

from emerge_config import *
from Source.SourceBase import *
from Source.VersionSystemSourceBase import *
import compiler


class SetupHelpr( object ):
    def __init__( self ):
        self.path = os.getenv( "PATH" )
        parser = argparse.ArgumentParser( )
        parser.add_argument( "--subst", action = "store_true" )
        parser.add_argument( "--get", action = "store_true" )
        parser.add_argument( "--print-banner", action = "store_true" )
        parser.add_argument( "--getenv", action = "store_true" )
        parser.add_argument("--mode", action = "store", choices = {"bat","powershell"})
        parser.add_argument( "rest", nargs = argparse.REMAINDER )
        self.args = parser.parse_args( )

    def run( self ):
        if self.args.subst:
            if emergeSettings.getboolean( "ShortPath", "EMERGE_USE_SHORT_PATH", False ):
                self.subst( os.path.abspath( emergeRoot( False ) ), "EMERGE_ROOT_DRIVE" )
                self.subst( emergeSettings.get( "Paths", "DOWNLOADDIR" ), "EMERGE_DOWNLOAD_DRIVE" )
                self.subst( emergeSettings.get( "Paths", "KDESVNDIR" ), "EMERGE_SVN_DRIVE" )
                self.subst( emergeSettings.get( "Paths", "KDEGITDIR" ), "EMERGE_GIT_DRIVE" )
        elif self.args.get:
            default = ""
            if len( self.args.rest ) == 3:
                default = self.args.rest[ 2 ]
            print( emergeSettings.get( self.args.rest[ 0 ], self.args.rest[ 1 ], default ) )
        elif self.args.print_banner:
            self.printBanner( )
        elif self.args.getenv:
            self.printEnv( )

    def subst( self, path, drive ):
        if not os.path.exists( path ):
            os.mkdir( path )
        command = "subst %s %s" % ( emergeSettings.get( "ShortPath", drive ), path)
        subprocess.Popen( command, stdout = subprocess.PIPE )

    def printBanner( self ):
        print( "KDEROOT     : %s" % emergeRoot( ) )
        print( "KDECOMPILER : %s" % compiler.getCompilerName( ) )
        print( "KDESVNDIR   : %s" % VersionSystemSourceBase.svnDir( ) )
        print( "KDEGITDIR   : %s" % VersionSystemSourceBase.gitDir( ) )
        print( "DOWNLOADDIR : %s" % SourceBase.downloadDir( ) )
        print( "PYTHONPATH  : %s" % emergeSettings.get( "Paths", "PYTHONPATH" ) )

    def printVar( self, key, val ):
        print( "%s=%s" % (key.upper( ), val) )

    def prependPath( self, var ):
        self.path = "%s;%s" % (var, self.path)

    def printEnv( self ):
        for var, value in emergeSettings.getSection( "Environment" ):
            self.printVar( var, value )
        self.printVar( "KDEROOT", emergeRoot())

        if self.args.mode == "bat":
            #needed for intel/msvc setup in bat
            self.printVar( "KDECOMPILER", emergeSettings.get( "General", "KDECOMPILER" ) )
            #needed for msvc setup in bat
            self.printVar( "EMERGE_ARCHITECTURE", emergeSettings.get( "General", "EMERGE_ARCHITECTURE" ) )

        if emergeSettings.getboolean( "General", "EMERGE_USE_CCACHE", False ):
            self.printVar( "CCACHE_DIR", emergeSettings.get( "Paths", "CCACHE_DIR", emergeSettings.get( "ShortPath",
                                                                                                        "EMERGE_ROOT_DRIVE" ) + "\\build\\CCACHE" ) )

        self.printVar( "GIT_SSH", "plink" )
        self.printVar( "SVN_SSH", "plink" )
        self.printVar( "HOME", os.getenv( "USERPROFILE" ) )

        self.printVar( "QT_PLUGIN_PATH", "%s;%s" % (
        os.path.join( emergeRoot( ), "plugins" ), os.path.join( emergeRoot( ), "lib", "kde4", "plugins" )) )
        self.printVar( "XDG_DATA_DIRS", os.path.join( emergeRoot( ), "share" ) )

        if compiler.isMinGW( ):
            if compiler.isX86( ):
                self.prependPath( os.path.join( emergeRoot( ), "mingw", "bin" ) )
            else:
                self.prependPath( os.path.join( emergeRoot( ), "mingw64", "bin" ) )

        self.prependPath( os.path.join( emergeRoot( ), "bin" ) )
        self.prependPath( os.path.join( emergeRoot( ), "emerge", "bin" ) )
        self.prependPath( os.path.join( emergeRoot( ), "dev-utils", "bin" ) )

        self.printVar( "PATH", self.path )


if __name__ == '__main__':
    helper = SetupHelpr( )
    helper.run( )

