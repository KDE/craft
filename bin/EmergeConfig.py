# -*- coding: utf-8 -*-
# central instance for managing settings regarding emerge
# copyright:
# Hannah von Reth <vonreth [AT] kde [DOT] org>

import sys
import subprocess
import configparser
import os
import platform
import re

emergeSettings = None

class EmergeStandardDirs( object ):
    __pathCache = dict( )
    __noShortPathCache = dict( )
    _allowShortpaths = True
    _SUBST = None

    @staticmethod
    def _deSubstPath(path):
        """desubstitude emerge short path"""

        if platform.system() != 'Windows':
            return path

        if emergeSettings and not emergeSettings.getboolean("General", "EMERGE_USE_SHORT_PATH"):
            return path
        drive , tail = os.path.splitdrive(path)
        drive = drive.upper()
        if EmergeStandardDirs._SUBST == None:
            tmp = subprocess.getoutput("subst").split("\n")
            EmergeStandardDirs._SUBST = dict()
            for s in tmp:
                if s != "":
                    key , val = s.split("\\: => ")
                    EmergeStandardDirs._SUBST[key] = val
        if drive in list(EmergeStandardDirs._SUBST.keys()):
            deSubst = EmergeStandardDirs._SUBST[drive] + tail
            return deSubst
        return path

    @staticmethod
    def _pathCache( ):
        if EmergeStandardDirs._allowShortpaths:
            return EmergeStandardDirs.__pathCache
        else:
            return EmergeStandardDirs.__noShortPathCache

    @staticmethod
    def allowShortpaths( allowd ):
        old = EmergeStandardDirs._allowShortpaths
        EmergeStandardDirs._allowShortpaths = allowd
        return old

    @staticmethod
    def isShortPathEnabled():
        return EmergeStandardDirs._allowShortpaths and emergeSettings.getboolean( "ShortPath", "EMERGE_USE_SHORT_PATH", False )

    @staticmethod
    def downloadDir( ):
        """ location of directory where fetched files are  stored """
        if not "DOWNLOADDIR" in EmergeStandardDirs._pathCache( ):
            if EmergeStandardDirs.isShortPathEnabled() and ("ShortPath", "EMERGE_DOWNLOAD_DRIVE" ) in emergeSettings:
                EmergeStandardDirs._pathCache( )[ "DOWNLOADDIR" ] = EmergeStandardDirs.nomalizePath(
                    emergeSettings.get( "ShortPath", "EMERGE_DOWNLOAD_DRIVE" ) )
            else:
                EmergeStandardDirs._pathCache( )[ "DOWNLOADDIR" ] = emergeSettings.get( "Paths", "DOWNLOADDIR",
                                                                                        os.path.join(
                                                                                            EmergeStandardDirs.emergeRoot( ),
                                                                                            "download" ) )
        return EmergeStandardDirs._pathCache( )[ "DOWNLOADDIR" ]

    @staticmethod
    def svnDir( ):
        if not "SVNDIR" in EmergeStandardDirs._pathCache( ):
            EmergeStandardDirs._pathCache( )[ "SVNDIR" ] = emergeSettings.get( "Paths", "KDESVNDIR",
                                                                                   os.path.join(
                                                                                   EmergeStandardDirs.downloadDir( ),
                                                                                   "svn" ) )
        return EmergeStandardDirs._pathCache( )[ "SVNDIR" ]

    @staticmethod
    def gitDir( ):
        if not "GITDIR" in EmergeStandardDirs._pathCache( ):
            if EmergeStandardDirs.isShortPathEnabled() and ("ShortPath", "EMERGE_GIT_DRIVE" ) in emergeSettings:
                EmergeStandardDirs._pathCache( )[ "GITDIR" ] = EmergeStandardDirs.nomalizePath(
                    emergeSettings.get( "ShortPath", "EMERGE_GIT_DRIVE" ) )
            else:
                EmergeStandardDirs._pathCache( )[ "GITDIR" ] = emergeSettings.get( "Paths", "KDEGITDIR",
                                                                                   os.path.join(
                                                                                       EmergeStandardDirs.downloadDir( ),
                                                                                       "git" ) )
        return EmergeStandardDirs._pathCache( )[ "GITDIR" ]

    @staticmethod
    def tmpDir():
        if not "TMPDIR" in EmergeStandardDirs._pathCache( ):
            EmergeStandardDirs._pathCache( )[ "TMPDIR" ] = emergeSettings.get( "Paths", "TMPDIR", os.path.join( EmergeStandardDirs.emergeRoot(), "tmp"))
        return EmergeStandardDirs._pathCache( )[ "TMPDIR" ]


    @staticmethod
    def nomalizePath( path ):
        if path.endswith( ":" ):
            path += "\\"
        return path


    @staticmethod
    def emergeRoot( ):
        if not "EMERGEROOT" in EmergeStandardDirs._pathCache( ):
            if EmergeStandardDirs.isShortPathEnabled() and ("ShortPath", "EMERGE_ROOT_DRIVE" ) in emergeSettings:
                EmergeStandardDirs._pathCache( )[ "EMERGEROOT" ] = EmergeStandardDirs.nomalizePath(
                    emergeSettings.get( "ShortPath", "EMERGE_ROOT_DRIVE" ) )
            else:
                EmergeStandardDirs._pathCache( )[ "EMERGEROOT" ] = os.path.abspath(
                    os.path.join( os.path.dirname( EmergeStandardDirs._deSubstPath(__file__ )), "..", ".." ) )
        return EmergeStandardDirs._pathCache( )[ "EMERGEROOT" ]

    @staticmethod
    def etcDir( ):
        return os.path.join( EmergeStandardDirs.emergeRoot( ), "etc" )

    @staticmethod
    def emergeRepositoryDir( ):
        return os.path.join( EmergeStandardDirs.emergeRoot( ), "emerge" )

    @staticmethod
    def etcPortageDir( ):
        """the etc directory for portage"""
        return os.path.join( EmergeStandardDirs.etcDir( ), "portage" )


class EmergeConfig( object ):
    variablePatern = re.compile( "\$\{[A-Za-z0-9_]*\}", re.IGNORECASE )

    def __init__( self, iniPath=None ):
        self._config = configparser.ConfigParser( )
        if iniPath:
            self.iniPath = iniPath
        else:
            with TemporaryUseShortpath(False):
                self.iniPath = os.path.join( EmergeStandardDirs.etcDir( ), "kdesettings.ini" )
        self._alias = dict( )
        self._readSettings( )

        if self.version < 2:
            self._setAliasesV1()
        if self.version < 3:
            self._setAliasesV2()

    def _setAliasesV2(self):
        self.addAlias( "Compile", "MakeProgram", "General", "EMERGE_MAKE_PROGRAM" )
        self.addAlias( "Compile", "BuildTests", "General", "EMERGE_BUILDTESTS" )
        self.addAlias( "Compile", "BuildType", "General", "EMERGE_BUILDTYPE" )
        self.addAlias( "Portage", "Ignores", "Portage", "PACKAGE_IGNORES" )


    def _setAliasesV1(self):
        self.setDefault( "General", "DUMP_SETTINGS", "False" )
        self.addAlias( "EmergeDebug", "Verbose", "General", "EMERGE_VERBOSE" )
        self.addAlias( "EmergeDebug", "MeasureTime", "General", "EMERGE_MEASURE_TIME" )
        self.addAlias( "General", "UseHardlinks", "General", "EMERGE_USE_SYMLINKS" )
        self.addAlias( "General", "WorkOffline", "General", "EMERGE_OFFLINE" )
        self.addAlias( "PortageVersions", "DefaultTarget", "General", "EMERGE_TARGET" )
        self.addAlias( "Paths", "Python", "Paths", "PYTHONPATH" )
        self.addAlias( "General", "Architecture", "General", "EMERGE_ARCHITECTURE" )
        self.addAlias( "Compile", "UseNinja", "General", "EMERGE_USE_NINJA" )
        self.addAlias( "Compile", "UseCCache", "General", "EMERGE_USE_CCACHE" )

    def _readSettings( self ):
        if not os.path.exists( self.iniPath ):
            print( "Could not find config: %s" % self.iniPath )
            return

        self._config.read( self.iniPath )
        clean = False
        #replace possible vatiables within a section
        while not clean:
            clean = True
            for section in self._config.keys( ):
                for key in self._config[ section ]:
                    val = self._config[ section ][ key ]
                    if self.variablePatern.match( val ):
                        clean = False
                        match = self.variablePatern.findall( val )[ 0 ]
                        self._config[ section ][ key ] = val.replace( match, self._config[ section ][ match[ 2:-1 ] ] )
        if not os.name == "nt":
            self.set("Portage", "Ignores", self.get("Portage", "Ignores")  + ";dev-util/.*;gnuwin32/.*")
            if self.get("General", "KDECompiler") == "linux-gcc":
                self.set("Portage", "Ignores", self.get("Portage", "Ignores")  + ";binary/.*;win32libs/.*")
                        
        if self.getboolean("QtSDK", "Enabled", "False"):
            self.set("Portage", "Ignores", self.get("Portage", "Ignores") + ";libs/qt.*")

    def __contains__( self, key ):
        return self.__contains_no_alias(key) or \
               (key in self._alias and self.__contains__(self._alias[key]))

    def __contains_no_alias( self, key ):
        return self._config and self._config.has_section( key[ 0 ] ) and key[ 1 ] in self._config[ key[ 0 ] ]

    @property
    def version(self):
        return int(self.get("Version", "EMERGE_SETTINGS_VERSION", 1))

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

        self._config[ group ][ key ]

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


class TemporaryUseShortpath(object):
    """Context handler for temporarily different shortpath setting"""
    def __init__(self, enabled):
        self.prev = EmergeStandardDirs.allowShortpaths(enabled)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, trback):
        EmergeStandardDirs.allowShortpaths(self.prev)



emergeSettings = EmergeConfig( )










