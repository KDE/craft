# -*- coding: utf-8 -*-
# central instance for managing settings regarding emerge
# copyright:
# Patrick von Reth <vonreth [AT] kde [DOT] org>

import sys
import subprocess

# The minimum python version for emerge please edit here
# if you add code that changes this requirement
MIN_PY_VERSION = (3, 4, 0)

if sys.version_info[ 0:3 ] < MIN_PY_VERSION:
    print( "Error: Python too old!", file= sys.stderr )
    print( "Emerge needs at least Python Version %s.%s.%s" % MIN_PY_VERSION, file= sys.stderr )
    print( "Please install it and adapt your kdesettings.bat", file= sys.stderr )
    exit( 1 )

import configparser
import os
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
        EmergeStandardDirs._allowShortpaths = allowd

    @staticmethod
    def downloadDir( ):
        """ location of directory where fetched files are  stored """
        if not "DOWNLOADDIR" in EmergeStandardDirs._pathCache( ):
            if EmergeStandardDirs._allowShortpaths and emergeSettings.getboolean( "ShortPath", "EMERGE_USE_SHORT_PATH",
                                                                                  False ):
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
            if EmergeStandardDirs._allowShortpaths and emergeSettings.getboolean( "ShortPath", "EMERGE_USE_SHORT_PATH",
                                                                                  False ):
                EmergeStandardDirs._pathCache( )[ "SVNDIR" ] = EmergeStandardDirs.nomalizePath(
                    emergeSettings.get( "ShortPath", "EMERGE_SVN_DRIVE" ) )
            else:
                EmergeStandardDirs._pathCache( )[ "SVNDIR" ] = emergeSettings.get( "Paths", "KDESVNDIR",
                                                                                   os.path.join(
                                                                                       EmergeStandardDirs.downloadDir( ),
                                                                                       "svn" ) )
        return EmergeStandardDirs._pathCache( )[ "SVNDIR" ]

    @staticmethod
    def gitDir( ):
        if not "GITDIR" in EmergeStandardDirs._pathCache( ):
            if EmergeStandardDirs._allowShortpaths and emergeSettings.getboolean( "ShortPath", "EMERGE_USE_SHORT_PATH",
                                                                                  False ):
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
            if EmergeStandardDirs._allowShortpaths and emergeSettings.getboolean( "ShortPath",
                                                                                  "EMERGE_USE_SHORT_PATH", False ):
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
    def etcPortageDir( ):
        """the etc directory for portage"""
        return os.path.join( EmergeStandardDirs.etcDir( ), "portage" )


class EmergeConfig( object ):
    variablePatern = re.compile( "\$\{[A-Za-z0-9_]*\}", re.IGNORECASE )

    def __init__( self ):
        self._config = None
        EmergeStandardDirs.allowShortpaths( False )
        self.iniPath = os.path.join( EmergeStandardDirs.etcDir( ), "kdesettings.ini" )
        EmergeStandardDirs.allowShortpaths( True )
        self._alias = dict( )
        self._readSettings( )

        self.setDefault( "General", "DUMP_SETTINGS", "False" )
        self.setDefault( "General", "EMERGE_OPTIONS", "")
        self.addAlias( "EmergeDebug", "Verbose", "General", "EMERGE_VERBOSE" )
        self.addAlias( "EmergeDebug", "MeasureTime", "General", "EMERGE_MEASURE_TIME" )
        self.addAlias( "General", "UseHardlinks", "General", "EMERGE_USE_SYMLINKS" )
        self.addAlias( "General", "WorkOffline", "General", "EMERGE_OFFLINE" )
        self.addAlias( "PortageVersions", "DefaultTarget", "General", "EMERGE_TARGET" )


    def _readSettings( self ):
        if not os.path.exists( self.iniPath ):
            print( "Could not find %s" % self.iniPath )
            exit( 1 )
        self._config = configparser.ConfigParser( )
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
                        
        if self.getboolean("QtSDK", "Enabled", "false"):
            self._blacklistQt()

    def _blacklistQt(self):
        self.set("Portage", "PACKAGE_IGNORES", self.get("Portage", "PACKAGE_IGNORES") + ";libs/qt;libs/qt5;dev-util/mingw-w64;binary/mysql-pkg" +
                ";libs/qt5/".join(["qtbase", "qtwebkit", "qttools", "qtscript", "qtactiveqt", "qtxmlpatterns", "qtdeclarative", "qtsvg", "qtgraphicaleffects", "qtimageformats", "qtmultimedia", "qtquick1", "qtwinextras"]))

    def __contains__( self, key ):
        return self._config and self._config.has_section( key[ 0 ] ) and key[ 1 ] in self._config[ key[ 0 ] ]


    def addAlias( self, group, key, destGroup, destKey ):
        self._alias[ (group, key) ] = (destGroup, destKey)

    def get( self, group, key, default = None ):
        if (group, key) in self:
            #print((group,key,self._config[ group ][ key ]))
            return self._config[ group ][ key ]
        if (group, key) in self._alias:
            dg, dk = self._alias[ (group, key) ]
            if (dg, dk) in self:
                print( "Warning: %s/%s is deprecated and has ben renamed to %s/%s" % (dg, dk, group, key ),
                       file = sys.stderr )
                return self.get( dg, dk, default )
        if default != None:
            self.set( group, key, default )
            return default
        print(group, key)
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
        if not self._config.has_section( group ):
            self._config.add_section( group )
        self._config[ group ][ key ] = str( value )


    def setDefault( self, group, key, value ):
        if not ( group, key ) in self:
            self.set( group, key, value )


    def dump( self ):
        with open( self.iniPath + ".dump", 'wt+' ) as configfile:
            self._config.write( configfile )


emergeSettings = EmergeConfig( )


