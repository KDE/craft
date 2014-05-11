# -*- coding: utf-8 -*-
# Helper script for substitution of paths, independent of cmd or powershell
# copyright:
# Patrick von Reth <vonreth [AT] kde [DOT] org>

import subprocess
import argparse

from EmergeConfig import *
import compiler


class SetupHelper( object ):
    def __init__( self ):
        self.env = None
        parser = argparse.ArgumentParser( )
        parser.add_argument( "--subst", action = "store_true" )
        parser.add_argument( "--get", action = "store_true" )
        parser.add_argument( "--print-banner", action = "store_true" )
        parser.add_argument( "--getenv", action = "store_true" )
        parser.add_argument( "--setup", action = "store_true" )
        parser.add_argument( "--mode", action = "store", choices = { "bat", "powershell" } )
        parser.add_argument( "rest", nargs = argparse.REMAINDER )
        self.args = parser.parse_args( )

    def run( self ):
        if self.args.subst:
            self.subst( )
        elif self.args.get:
            default = ""
            if len( self.args.rest ) == 3:
                default = self.args.rest[ 2 ]
            print( emergeSettings.get( self.args.rest[ 0 ], self.args.rest[ 1 ], default ) )
        elif self.args.print_banner:
            self.printBanner( )
        elif self.args.getenv:
            self.printEnv( )
        elif self.args.setup:
            self.subst( )
            self.printEnv( )
            self.printBanner( )


    def subst( self, ):
        def _subst( path, drive ):
            if not os.path.exists( path ):
                os.mkdir( path )
            command = "subst %s %s" % ( emergeSettings.get( "ShortPath", drive ), path)
            subprocess.getoutput( command )

        if emergeSettings.getboolean( "ShortPath", "EMERGE_USE_SHORT_PATH", False ):
            EmergeStandardDirs.allowShortpaths( False )
            _subst( EmergeStandardDirs.emergeRoot( ), "EMERGE_ROOT_DRIVE" )
            _subst( EmergeStandardDirs.downloadDir( ), "EMERGE_DOWNLOAD_DRIVE" )
            _subst( EmergeStandardDirs.svnDir( ), "EMERGE_SVN_DRIVE" )
            _subst( EmergeStandardDirs.gitDir( ), "EMERGE_GIT_DRIVE" )
            EmergeStandardDirs.allowShortpaths( True )

    def printBanner( self ):
        print( "KDEROOT     : %s" % EmergeStandardDirs.emergeRoot( ), file = sys.stderr )
        print( "KDECOMPILER : %s" % compiler.getCompilerName( ), file = sys.stderr )
        print( "KDESVNDIR   : %s" % EmergeStandardDirs.svnDir( ), file = sys.stderr )
        print( "KDEGITDIR   : %s" % EmergeStandardDirs.gitDir( ), file = sys.stderr )
        print( "DOWNLOADDIR : %s" % EmergeStandardDirs.downloadDir( ), file = sys.stderr )
        print( "PYTHONPATH  : %s" % emergeSettings.get( "Paths", "PYTHONPATH" ), file = sys.stderr )

    def addEnvVar( self, key, val ):
        self.env[ key ] = val

    def prependPath( self, var ):
        self.env[ "Path" ] = "%s;%s" % (var, self.env[ "Path" ])


    def stringToEnv( self, string ):
        out = dict( )
        for line in string.split( "\n" ):
            key, value = line.strip( ).split( "=", 1 )
            out[ key ] = value
        return out

    def getEnv( self ):
        out = dict( )
        if compiler.isMSVC( ):
            compilerDirs = { "msvc2010": "VS100COMNTOOLS", "msvc2012": "VS110COMNTOOLS", "msvc2013": "VS120COMNTOOLS" }
            architectures = { "x86": "x86", "x64": "amd64" }
            status, result = subprocess.getstatusoutput( "\"%s\\..\\..\\VC\\vcvarsall.bat\" %s > NUL && set" % (
                os.getenv( compilerDirs[ compiler.getCompilerName( ) ] ), architectures[ compiler.architecture( ) ]) )
            if status != 0:
                print( "Failed to setup msvc compiler", file = sys.stderr )
            out = self.stringToEnv( result )

        elif compiler.isIntel( ):
            architectures = { "x86": "ia32", "x64": "intel64" }
            programFiles = os.getenv( "ProgramFiles(x86)" ) or os.getenv( "ProgramFiles" )
            status, result = subprocess.getstatusoutput(
                "\"%s\\Intel\\Composer XE\\bin\\compilervars.bat\" %s > NUL && set" % (
                    programFiles, architectures[ compiler.architecture( ) ]) )
            if status != 0:
                print( "Failed to setup intel compiler", file = sys.stderr )
            out = self.stringToEnv( result )
        elif compiler.isMinGW( ):
            out = { "Path": os.getenv( "Path" ) }
        return out


    def printEnv( self ):
        self.env = self.getEnv( )

        self.addEnvVar( "KDEROOT", EmergeStandardDirs.emergeRoot( ) )

        if emergeSettings.getboolean( "General", "EMERGE_USE_CCACHE", False ):
            self.addEnvVar( "CCACHE_DIR",
                            emergeSettings.get( "Paths", "CCACHE_DIR", os.path.join( emergeSettings.get( "ShortPath",
                                                                                                         "EMERGE_ROOT_DRIVE" ),
                                                                                     "build", "CCACHE" ) ) )

        self.addEnvVar( "GIT_SSH", "plink" )
        self.addEnvVar( "SVN_SSH", "plink" )
        self.addEnvVar( "HOME", os.getenv( "USERPROFILE" ) )

        self.addEnvVar( "PKG_CONFIG_PATH", os.path.join( EmergeStandardDirs.emergeRoot( ), "lib", "pkgconfig" ) )

        self.addEnvVar( "QT_PLUGIN_PATH", "%s;%s" % (
            os.path.join( EmergeStandardDirs.emergeRoot( ), "plugins" ),
            os.path.join( EmergeStandardDirs.emergeRoot( ), "lib", "kde4", "plugins" )) )
        self.addEnvVar( "XDG_DATA_DIRS", os.path.join( EmergeStandardDirs.emergeRoot( ), "share" ) )

        if compiler.isMinGW( ):
            if compiler.isX86( ):
                self.prependPath( os.path.join( EmergeStandardDirs.emergeRoot( ), "mingw", "bin" ) )
            else:
                self.prependPath( os.path.join( EmergeStandardDirs.emergeRoot( ), "mingw64", "bin" ) )

        self.prependPath( os.path.join( EmergeStandardDirs.emergeRoot( ), "bin" ) )
        if self.args.mode == "bat":  #don't put emerge.bat in path when using powershell
            self.prependPath( os.path.join( EmergeStandardDirs.emergeRoot( ), "emerge", "bin" ) )
        self.prependPath( os.path.join( EmergeStandardDirs.emergeRoot( ), "dev-utils", "bin" ) )


        for var, value in emergeSettings.getSection( "Environment" ):#set and overide existing values
            self.addEnvVar( var, value )
        for key, val in self.env.items( ):
            print( "%s=%s" % (key, val) )


if __name__ == '__main__':
    helper = SetupHelper( )
    helper.run( )

