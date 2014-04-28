# -*- coding: utf-8 -*-
# this package contains functions to easily set versions for packages like qt5 or kde
# copyright:
# Patrick von Reth <vonreth [AT] kde [DOT] org>

from emerge_config import *
import utils


class VersionInfo( object ):
    _VERSION_INFOS = dict( )
    _VERSION_INFOS_HINTS = dict( )

    def __init__( self, parent ):
        self.subinfo = parent
        self.__defaulVersions = None

    @property
    def _defaulVersions( self ):
        if self.__defaulVersions is None:
            name = self.subinfo.parent.filename
            if name in VersionInfo._VERSION_INFOS_HINTS:
                if VersionInfo._VERSION_INFOS_HINTS[ name ] == None:
                    return None
                else:
                    #utils.debug("Using cached version info for %s in %s" % (name, _VERSION_INFOS_HINTS[ name ]),0)
                    return VersionInfo._VERSION_INFOS[ VersionInfo._VERSION_INFOS_HINTS[ name ] ]
            root = os.path.dirname( name )

            dirs = [ os.path.join( root, "version.ini" ), os.path.join( root, "..", "version.ini" ),
                     os.path.join( root, "..", "..", "version.ini" ) ]

            for iniPath in dirs:
                iniPath = os.path.abspath( iniPath )
                if iniPath in VersionInfo._VERSION_INFOS.keys( ):
                    VersionInfo._VERSION_INFOS_HINTS[ name ] = iniPath
                    utils.debug( "Found a version info for %s in cache" % name, 1 )
                    return VersionInfo._VERSION_INFOS[ iniPath ]
                elif os.path.exists( iniPath ):
                    config = configparser.ConfigParser( )
                    config.read( iniPath )
                    VersionInfo._VERSION_INFOS[ iniPath ] = config
                    VersionInfo._VERSION_INFOS_HINTS[ name ] = iniPath
                    utils.debug( "Found a version info for %s in %s" % (name, iniPath), 1 )
                    return config
            VersionInfo._VERSION_INFOS_HINTS[ name ] = None
        return self.__defaulVersions


    def _getVersionInfo( self, key, name = None ):
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
        return self.subinfo.package
        
    