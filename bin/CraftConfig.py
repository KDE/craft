# -*- coding: utf-8 -*-
# central instance for managing settings regarding craft
# copyright:
# Hannah von Reth <vonreth [AT] kde [DOT] org>

import sys
import subprocess
import configparser
import os
import platform
import re

import atexit

craftSettings = None

class CraftStandardDirs( object ):
    __pathCache = dict( )
    __noShortPathCache = dict( )
    _allowShortpaths = True
    _SUBST = None

    @staticmethod
    def _deSubstPath(path):
        """desubstitude craft short path"""

        if platform.system() != 'Windows':
            return path
        drive , tail = os.path.splitdrive(path)
        drive = drive.upper()
        if CraftStandardDirs._SUBST == None:
            tmp = subprocess.getoutput("subst").split("\n")
            CraftStandardDirs._SUBST = dict()
            for s in tmp:
                if s != "":
                    key , val = s.split("\\: => ")
                    CraftStandardDirs._SUBST[key] = val
        if drive in CraftStandardDirs._SUBST:
            deSubst = CraftStandardDirs._SUBST[drive] + tail
            return deSubst
        return path

    @staticmethod
    def _pathCache( ):
        if CraftStandardDirs._allowShortpaths:
            return CraftStandardDirs.__pathCache
        else:
            return CraftStandardDirs.__noShortPathCache

    @staticmethod
    def allowShortpaths( allowd ):
        old = CraftStandardDirs._allowShortpaths
        CraftStandardDirs._allowShortpaths = allowd
        return old

    @staticmethod
    def isShortPathEnabled():
        return CraftStandardDirs._allowShortpaths and craftSettings.getboolean( "ShortPath", "Enabled", False )

    @staticmethod
    def downloadDir( ):
        """ location of directory where fetched files are  stored """
        if not "DOWNLOADDIR" in CraftStandardDirs._pathCache( ):
            if CraftStandardDirs.isShortPathEnabled() and ("ShortPath", "DownloadDrive" ) in craftSettings:
                CraftStandardDirs._pathCache( )[ "DOWNLOADDIR" ] = CraftStandardDirs.nomalizePath(
                    craftSettings.get( "ShortPath", "DownloadDrive" ) )
            else:
                CraftStandardDirs._pathCache( )[ "DOWNLOADDIR" ] = craftSettings.get( "Paths", "DOWNLOADDIR",
                                                                                        os.path.join(
                                                                                            CraftStandardDirs.craftRoot( ),
                                                                                            "download" ) )
        return CraftStandardDirs._pathCache( )[ "DOWNLOADDIR" ]

    @staticmethod
    def svnDir( ):
        if not "SVNDIR" in CraftStandardDirs._pathCache( ):
            CraftStandardDirs._pathCache( )[ "SVNDIR" ] = craftSettings.get( "Paths", "KDESVNDIR",
                                                                                   os.path.join(
                                                                                   CraftStandardDirs.downloadDir( ),
                                                                                   "svn" ) )
        return CraftStandardDirs._pathCache( )[ "SVNDIR" ]

    @staticmethod
    def gitDir( ):
        if not "GITDIR" in CraftStandardDirs._pathCache( ):
            if CraftStandardDirs.isShortPathEnabled() and ("ShortPath", "GitDrive" ) in craftSettings:
                CraftStandardDirs._pathCache( )[ "GITDIR" ] = CraftStandardDirs.nomalizePath(
                    craftSettings.get( "ShortPath", "GitDrive" ) )
            else:
                CraftStandardDirs._pathCache( )[ "GITDIR" ] = craftSettings.get( "Paths", "KDEGITDIR",
                                                                                   os.path.join(
                                                                                       CraftStandardDirs.downloadDir( ),
                                                                                       "git" ) )
        return CraftStandardDirs._pathCache( )[ "GITDIR" ]

    @staticmethod
    def tmpDir():
        if not "TMPDIR" in CraftStandardDirs._pathCache( ):
            CraftStandardDirs._pathCache( )[ "TMPDIR" ] = craftSettings.get( "Paths", "TMPDIR", os.path.join( CraftStandardDirs.craftRoot(), "tmp"))
        return CraftStandardDirs._pathCache( )[ "TMPDIR" ]


    @staticmethod
    def nomalizePath( path ):
        if path.endswith( ":" ):
            path += "\\"
        return path


    @staticmethod
    def craftRoot( ):
        if not "EMERGEROOT" in CraftStandardDirs._pathCache( ):
            if CraftStandardDirs.isShortPathEnabled() and ("ShortPath", "RootDrive" ) in craftSettings:
                CraftStandardDirs._pathCache( )[ "EMERGEROOT" ] = CraftStandardDirs.nomalizePath(
                    craftSettings.get( "ShortPath", "RootDrive" ) )
            else:
                CraftStandardDirs._pathCache( )[ "EMERGEROOT" ] = os.path.abspath(
                    os.path.join( os.path.dirname( CraftStandardDirs._deSubstPath(__file__ )), "..", ".." ) )
        return CraftStandardDirs._pathCache( )[ "EMERGEROOT" ]

    @staticmethod
    def etcDir( ):
        return os.path.join( CraftStandardDirs.craftRoot( ), "etc" )

    @staticmethod
    def craftBin():
        return os.path.join(CraftStandardDirs.craftRoot(), os.path.dirname(__file__))

    @staticmethod
    def craftRepositoryDir( ):
        return os.path.join(CraftStandardDirs.craftBin(), "..", "portage" )

    @staticmethod
    def etcPortageDir( ):
        """the etc directory for portage"""
        return os.path.join( CraftStandardDirs.etcDir( ), "portage" )

    @staticmethod
    def msysDir():
        if ("Paths", "Msys") in craftSettings:
            return craftSettings.get("Paths", "Msys")
        return os.path.join(CraftStandardDirs.craftRoot(), "msys")


class CraftConfig( object ):
    variablePatern = re.compile( "\$\{[A-Za-z0-9_]*\}", re.IGNORECASE )

    def __init__( self, iniPath=None ):
        self._config = configparser.ConfigParser( interpolation=configparser.ExtendedInterpolation() )
        if iniPath:
            self.iniPath = iniPath
        else:
            with TemporaryUseShortpath(False):
                self.iniPath = os.path.join( CraftStandardDirs.etcDir( ), "kdesettings.ini" )
        self._alias = dict( )
        self._readSettings( )

        if self.version < 3:
            self._setAliasesV2()

        if self.version < 4:
            self._setAliasesV3()

    def _setAliasesV3(self):
        self.addAlias("General", "Options", "General", "EMERGE_OPTIONS")
        self.addAlias("CraftDebug", "LogDir", "General", "EMERGE_LOG_DIR")
        self.addAlias("ShortPath", "GitDrive", "ShortPath", "EMERGE_GIT_DRIVE")
        self.addAlias("ShortPath", "RootDrive", "ShortPath", "EMERGE_ROOT_DRIVE")
        self.addAlias("ShortPath", "DownloadDrive", "ShortPath", "EMERGE_DOWNLOAD_DRIVE")
        self.addAlias("ShortPath", "Enabled", "ShortPath", "EMERGE_USE_SHORT_PATH")

    def _setAliasesV2(self):
        self.addAlias( "Compile", "MakeProgram", "General", "EMERGE_MAKE_PROGRAM" )
        self.addAlias( "Compile", "BuildTests", "General", "EMERGE_BUILDTESTS" )
        self.addAlias( "Compile", "BuildType", "General", "EMERGE_BUILDTYPE" )
        self.addAlias( "Portage", "Ignores", "Portage", "PACKAGE_IGNORES" )
        self.addAlias("Package", "UseCache", "ContinuousIntegration", "UseCache")
        self.addAlias("Package", "CreateCache", "ContinuousIntegration", "UseCache")
        self.addAlias("Package", "CacheDir", "ContinuousIntegration", "CacheDir")
        self.addAlias("Package", "RepositoryUrl", "ContinuousIntegration", "RepositoryUrl")


    def _readSettings( self ):
        if not os.path.exists( self.iniPath ):
            print( "Could not find config: %s" % self.iniPath )
            return

        self._config.read( self.iniPath )
        if not "Variables" in self._config.sections():
            self._config.add_section("Variables")
        for  key, value in {
            "CraftRoot" : os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")),
            "CraftDir" : os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        }.items():
            if not key in self._config["Variables"]:
                self._config["Variables"][key] = value
        if not os.name == "nt":
            self.set("Portage", "Ignores", self.get("Portage", "Ignores")  + ";dev-util/.*;gnuwin32/.*")

    def __contains__( self, key ):
        return self.__contains_no_alias(key) or \
               (key in self._alias and self.__contains__(self._alias[key]))

    def __contains_no_alias( self, key ):
        return self._config and self._config.has_section( key[ 0 ] ) and key[ 1 ] in self._config[ key[ 0 ] ]

    @property
    def version(self):
        return int(self.get("Version", "ConfigVersion", 2))

    def addAlias( self, group, key, destGroup, destKey ):
        self._alias[ (group, key) ] = (destGroup, destKey)

    def get( self, group, key, default = None ):
        if self.__contains_no_alias((group, key)):
            #print((group,key,self._config[ group ][ key ]))
            return self._config[ group ][ key ]

        if (group, key) in self._alias:
            dg, dk = self._alias[ (group, key) ]
            if (dg, dk) in self:
                print( "Warning: %s/%s is deprecated and has been renamed to %s/%s, please update your kdesettings.ini" % (dg, dk, group, key ),
                       file = sys.stderr )
                val = self.get( dg, dk, default )
                if not group in self._config.sections():
                    self._config.add_section(group)
                self._config[ group ][ key ] = val
                return val

        if default != None:
            return default
        print("Failed to find")
        print("\t[%s]" % group)
        print("\t%s = ..." % key)
        print("in your kdesettings.ini")
        exit(1)

    def getSection( self, group ):
        if self._config.has_section( group ):
            return self._config.items( group )
        else:
            return [ ]

    def getboolean( self, group, key, default = False ):
        val = self.get( group, key, str( default ) )
        return self._config._convert_to_boolean( val )


    def set( self, group, key, value ):
        if value is None:
            return
        if not self._config.has_section( group ):
            self._config.add_section( group )
        self._config[ group ][ key ] = str( value )


    def setDefault( self, group, key, value ):
        if not ( group, key ) in self:
            self.set( group, key, value )


    def dump( self ):
        with open( self.iniPath + ".dump", 'wt+' ) as configfile:
            self._config.write( configfile )


    @staticmethod
    @atexit.register
    def _dump():
        if craftSettings.getboolean("CraftDebug", "DumpSettings", False):
            craftSettings.dump()


class TemporaryUseShortpath(object):
    """Context handler for temporarily different shortpath setting"""
    def __init__(self, enabled):
        self.prev = CraftStandardDirs.allowShortpaths(enabled)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trback):
        CraftStandardDirs.allowShortpaths(self.prev)



craftSettings = CraftConfig( )









