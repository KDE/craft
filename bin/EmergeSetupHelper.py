# -*- coding: utf-8 -*-
# Helper script for substitution of paths, independent of cmd or powershell
# copyright:
# Hannah von Reth <vonreth [AT] kde [DOT] org>

import subprocess
import argparse

from EmergeConfig import *
import compiler


# The minimum python version for emerge please edit here
# if you add code that changes this requirement
MIN_PY_VERSION = (3, 5, 0)

if sys.version_info[ 0:3 ] < MIN_PY_VERSION:
    print( "Error: Python too old!", file= sys.stderr )
    print( "Emerge needs at least Python Version %s.%s.%s" % MIN_PY_VERSION, file= sys.stderr )
    print( "Please install it and adapt your kdesettings.ini", file= sys.stderr )
    exit( 1 )

class SetupHelper( object ):
    def __init__( self ):
        self.env = None
        parser = argparse.ArgumentParser( )
        parser.add_argument( "--subst", action = "store_true" )
        parser.add_argument( "--get", action = "store_true" )
        parser.add_argument( "--print-banner", action = "store_true" )
        parser.add_argument( "--getenv", action = "store_true" )
        parser.add_argument( "--setup", action = "store_true" )
        parser.add_argument( "--mode", action = "store", choices = { "bat", "powershell", "bash" } )
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
            with TemporaryUseShortpath( False):
                if ("ShortPath", "EMERGE_ROOT_DRIVE") in emergeSettings:
                    _subst( EmergeStandardDirs.emergeRoot( ), "EMERGE_ROOT_DRIVE" )
                if ("ShortPath", "EMERGE_DOWNLOAD_DRIVE") in emergeSettings:
                    _subst( EmergeStandardDirs.downloadDir( ), "EMERGE_DOWNLOAD_DRIVE" )
                if ("ShortPath", "EMERGE_GIT_DRIVE") in emergeSettings:
                    _subst( EmergeStandardDirs.gitDir( ), "EMERGE_GIT_DRIVE" )

    def printBanner( self ):
        print( "KDEROOT     : %s" % EmergeStandardDirs.emergeRoot( ), file = sys.stderr )
        print( "KDECOMPILER : %s" % compiler.getCompilerName( ), file = sys.stderr )
        print( "KDESVNDIR   : %s" % EmergeStandardDirs.svnDir( ), file = sys.stderr )
        print( "KDEGITDIR   : %s" % EmergeStandardDirs.gitDir( ), file = sys.stderr )
        print( "DOWNLOADDIR : %s" % EmergeStandardDirs.downloadDir( ), file = sys.stderr )
        print( "PYTHONPATH  : %s" % emergeSettings.get( "Paths", "Python" ), file = sys.stderr )

    def addEnvVar( self, key, val ):
        self.env[ key ] = val

    def prependPath( self, key, var ):
        if not type(var) == list:
            var = [var]
        if key in self.env:
            var += [self.env[ key ]]
        self.env[ key ] = os.path.pathsep.join( var )

    def stringToEnv( self, string ):
        out = dict( )
        for line in string.split( "\n" ):
            key, value = line.strip( ).split( "=", 1 )
            out[ key ] = value
        return out

    def getEnv( self ):
        if compiler.isMSVC( ):
            compilerDirs = {
                "msvc2010": "VS100COMNTOOLS",
                "msvc2012": "VS110COMNTOOLS",
                "msvc2013": "VS120COMNTOOLS",
                "msvc2015": "VS140COMNTOOLS"
            }
            architectures = { "x86": "x86", "x64": "amd64", "x64_cross": "x86_amd64" }
            crossmodifier = ""
            if not compiler.isNative(): crossmodifier="_cross"
            status, result = subprocess.getstatusoutput( "\"%s\\..\\..\\VC\\vcvarsall.bat\" %s > NUL && set" % (
                os.getenv( compilerDirs[ compiler.getCompilerName( ) ] ), architectures[ compiler.architecture( ) + crossmodifier ]) )
            if status != 0:
                print( "Failed to setup msvc compiler", file = sys.stderr )
                exit(1)
            return self.stringToEnv( result )

        elif compiler.isIntel( ):
            architectures = { "x86": "ia32", "x64": "intel64" }
            programFiles = os.getenv( "ProgramFiles(x86)" ) or os.getenv( "ProgramFiles" )
            status, result = subprocess.getstatusoutput(
                "\"%s\\Intel\\Composer XE\\bin\\compilervars.bat\" %s > NUL && set" % (
                    programFiles, architectures[ compiler.architecture( ) ]) )
            if status != 0:
                print( "Failed to setup intel compiler", file = sys.stderr )
                exit(1)
            return self.stringToEnv( result )
        return os.environ


    def setXDG(self):
        self.addEnvVar( "XDG_DATA_DIRS", os.path.pathsep.join(
            [
                os.path.join( EmergeStandardDirs.emergeRoot( ), "share" ),
                os.getenv("XDG_DATA_DIRS")
            ]))
        if self.args.mode == "bash":
            self.addEnvVar( "XDG_CONFIG_DIRS", os.path.pathsep.join(
                [
                    os.path.join( EmergeStandardDirs.emergeRoot( ), "etc", "xdg" ),
                    os.getenv("XDG_CONFIG_DIRS")
                ]))
            self.addEnvVar( "XDG_DATA_HOME", os.path.join( EmergeStandardDirs.emergeRoot( ), "home", os.getenv("USER"), ".local5", "share" ))
            self.addEnvVar( "XDG_CONFIG_HOME", os.path.join( EmergeStandardDirs.emergeRoot( ), "home", os.getenv("USER"), ".config" ))
            self.addEnvVar( "XDG_CACHE_HOME", os.path.join( EmergeStandardDirs.emergeRoot( ), "home", os.getenv("USER"), ".cache" ))




    def printEnv( self ):
        self.env = self.getEnv( )
        self.version = int(emergeSettings.get("Version", "EMERGE_SETTINGS_VERSION"))

        self.addEnvVar( "KDEROOT", EmergeStandardDirs.emergeRoot( ) )

        if emergeSettings.getboolean( "Compile", "UseCCache", False ):
            self.addEnvVar( "CCACHE_DIR",
                            emergeSettings.get( "Paths", "CCACHE_DIR", os.path.join( EmergeStandardDirs.emergeRoot( ),
                                                                                     "build", "CCACHE" ) ) )

        if self.version < 2:
            self.addEnvVar( "GIT_SSH", "plink" )
            self.addEnvVar( "SVN_SSH", "plink" )

        if not "HOME" in self.env.keys():
            self.addEnvVar( "HOME", os.getenv( "USERPROFILE" ) )

        self.prependPath( "PKG_CONFIG_PATH", os.path.join( EmergeStandardDirs.emergeRoot( ), "lib", "pkgconfig" ))

        self.prependPath( "QT_PLUGIN_PATH", [ os.path.join( EmergeStandardDirs.emergeRoot( ), "plugins" ),
                                              os.path.join( EmergeStandardDirs.emergeRoot( ), "lib", "plugins" ),
                                              os.path.join( EmergeStandardDirs.emergeRoot( ), "lib64", "plugins" ),
                                              os.path.join( EmergeStandardDirs.emergeRoot( ), "lib", "x86_64-linux-gnu", "plugins" ),
                                              os.path.join( EmergeStandardDirs.emergeRoot( ), "lib", "plugin" )
                                            ])

        self.prependPath( "QML2_IMPORT_PATH", [ os.path.join( EmergeStandardDirs.emergeRoot(), "lib", "qml"),os.path.join( EmergeStandardDirs.emergeRoot(), "lib64", "qml"),
                                                os.path.join( EmergeStandardDirs.emergeRoot(), "lib", "x86_64-linux-gnu", "qml")
                                                ])
        self.prependPath("QML_IMPORT_PATH", self.env["QML2_IMPORT_PATH"])



        if self.args.mode == "bash":
            self.prependPath("LD_LIBRARY_PATH", [os.path.join(EmergeStandardDirs.emergeRoot(), "lib")])

        self.setXDG()

        if emergeSettings.getboolean("QtSDK", "Enabled", "false"):
            self.prependPath( "PATH", os.path.join( emergeSettings.get("QtSDK", "Path") , emergeSettings.get("QtSDK", "Version"), emergeSettings.get("QtSDK", "Compiler"), "bin"))

        if compiler.isMinGW( ):
            if not emergeSettings.getboolean("QtSDK", "Enabled", "false"):
                if compiler.isX86( ):
                    self.prependPath( "PATH", os.path.join( EmergeStandardDirs.emergeRoot( ), "mingw", "bin" ) )
                else:
                    self.prependPath( "PATH", os.path.join( EmergeStandardDirs.emergeRoot( ), "mingw64", "bin" ) )
            else:
                self.prependPath( "PATH", os.path.join( emergeSettings.get("QtSDK", "Path") ,"Tools", emergeSettings.get("QtSDK", "Compiler"), "bin" ))

        if self.args.mode in ["bat", "bash"]:  #don't put emerge.bat in path when using powershell
            self.prependPath( "PATH", os.path.join( EmergeStandardDirs.emergeRoot( ), "emerge", "bin" ) )
        self.prependPath( "PATH", os.path.join( EmergeStandardDirs.emergeRoot( ), "dev-utils", "bin" ) )


        #make sure thate emergeroot bin is the first to look for dlls etc
        self.prependPath( "PATH", os.path.join( EmergeStandardDirs.emergeRoot( ), "bin" ) )

        # add python site packages to pythonpath
        self.prependPath( "PythonPath",  os.path.join( EmergeStandardDirs.emergeRoot( ), "lib", "site-packages"))

        for var, value in emergeSettings.getSection( "Environment" ):  #set and overide existing values
            self.addEnvVar( var, value )
        for key, val in self.env.items( ):
            print( "%s=%s" % (key, val) )


if __name__ == '__main__':
    helper = SetupHelper( )
    helper.run( )

