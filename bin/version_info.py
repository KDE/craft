# -*- coding: utf-8 -*-
# this package contains functions to easily set versions for packages like qt5 or kde
# copyright:
# Patrick von Reth <vonreth [AT] kde [DOT] org>

import configparser
import os

import utils
from emerge_config import *
import utils


_VERSION_INFOS = dict( )
_VERSION_INFOS_HINTS = dict( )


class VersionInfo( object ):
    def __init__( self ):
        self._package = None
        self._defaulVersions = None

    def __getVersionConfig( self, name ):
        global _VERSION_INFOS
        global _VERSION_INFOS_HINTS
        if name in _VERSION_INFOS_HINTS:
            if _VERSION_INFOS_HINTS[ name ] == None:
                return None
            else:
                return _VERSION_INFOS[ _VERSION_INFOS_HINTS[ name ] ]
        root = os.path.dirname( name )
        dirs = [ os.path.join( root, "version.ini" ), os.path.join( root, "..", "version.ini" ) ]

        for iniPath in dirs:
            if iniPath in _VERSION_INFOS:
                return _VERSION_INFOS[ iniPath ]
            if os.path.exists( iniPath ):
                config = configparser.ConfigParser( )
                config.read( iniPath )
                _VERSION_INFOS[ iniPath ] = config
                _VERSION_INFOS_HINTS[ name ] = iniPath
                return config
        _VERSION_INFOS_HINTS[ name ] = None


    def setupDefaultVersions( self, filename ):
        self._defaulVersions = self.__getVersionConfig( filename )
        self._package = os.path.basename( filename )[:-3]


    def _getVersionInfo( self, key, name = None ):
        if self._defaulVersions == None:
            info = name
            if info == None:
                info = key
            utils.fail( "Please calls setupDefaultVersions(__file__) before calling self.%s()" % info )
        if self._defaulVersions.has_section( "General" ) and key in self._defaulVersions[ "General" ]:
            return self._defaulVersions[ "General" ][ key ]
        return ""

    def tags( self ):
        return self._getVersionInfo( "tags" ).split( ";" )

    def branches( self ):
        return self._getVersionInfo( "branches" ).split( ";" )

    def tarballs( self ):
        return self._getVersionInfo( "tarballs" ).split( ";" )

    def defaultTarget( self ):
        name = self._getVersionInfo( "name", "defaultTarget" )
        if ("PortageVersions", name) in emergeSettings:
            return emergeSettings.get( "PortageVersions", name )
        return self._getVersionInfo( "defaulttarget" )

    def packageName( self ):
        self._getVersionInfo( "", "packageName" )
        return self._package
        
    