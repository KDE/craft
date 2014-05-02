# -*- coding: utf-8 -*-
# central instance for managing settings regarding emerge
# copyright:
# Patrick von Reth <vonreth [AT] kde [DOT] org>

import configparser
import os
import re
import sys

emergeSettings = None

def nomalizePath(path):
    if path.endswith( ":" ):
        path += "\\"
    return path

def emergeRoot( allowShortpath = True ):
    if allowShortpath and not emergeSettings is None and emergeSettings.getboolean("ShortPath", "EMERGE_USE_SHORT_PATH", False):
        return  nomalizePath(emergeSettings.get( "ShortPath", "EMERGE_ROOT_DRIVE" ))
    return os.path.abspath( os.path.join( os.path.dirname( sys.argv[ 0 ] ), "..", ".." ) )


def etcDir( allowShortpath = True ):
    return os.path.join( emergeRoot( allowShortpath ), "etc" )


def etcPortageDir( allowShortpath = True ):
    """the etc directory for portage"""
    return os.path.join( etcDir( allowShortpath ), "portage" )


class EmergeConfig( object ):
    variablePatern = re.compile( "\$\{[A-Za-z0-9_]*\}", re.IGNORECASE )

    def __init__( self ):
        self._config = None
        self.iniPath = os.path.join( etcDir( False ), "kdesettings.ini" )
        self._alias = dict( )
        self._readSettings( )

        self.setDefault( "General", "DUMP_SETTINGS", "False" )
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


    def __contains__( self, key ):
        return self._config and self._config.has_section( key[ 0 ] ) and key[ 1 ] in self._config[ key[ 0 ] ]


    def addAlias( self, group, key, destGroup, destKey ):
        self._alias[ (group, key) ] = (destGroup, destKey)

    def get( self, group, key, default = None ):
        if self.__contains__( (group, key) ):
            #print((group,key,self._config[ group ][ key ]))
            return self._config[ group ][ key ]
        if (group, key) in self._alias:
            dg, dk = self._alias[ (group, key) ]
            if (dg, dk) in self:
                print( "Warning: %s/%s is deprecated and has ben renamed to %s/%s" % (dg, dk, group, key ), file = sys.stderr )
                return self.get( dg, dk, default )
        if default != None:
            self.set( group, key, default )
            return default
        self._config[ group ][ key ]

    def getboolean(self,  group, key, default = False):
        val = self.get(group,key,str(default))
        return self._config._convert_to_boolean(val)


    def set( self, group, key, value ):
        if not self._config.has_section(group):
            self._config.add_section(group)
        self._config[ group ][ key ] = str(value)
        if self.get( "General", "DUMP_SETTINGS", "False" ) == "True":
            with open( self.iniPath + ".dump", 'wt+' ) as configfile:
                self._config.write( configfile )


    def setDefault( self, group, key, value ):
        if not ( group, key ) in self:
            self.set( group, key, value )


emergeSettings = EmergeConfig( )


