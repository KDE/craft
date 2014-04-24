# -*- coding: utf-8 -*-
# copyright:
# Patrick von Reth <vonreth [AT] kde [DOT] org>

import configparser
import os
import re
import sys

emergeSettings = None

def emergeRoot():
    if not emergeSettings is None and emergeSettings.get("ShortPath","EMERGE_USE_SHORT_PATH", "False") == "True":
        path = emergeSettings.get("ShortPath","EMERGE_ROOT_DRIVE")
        if path.endswith(":"):
            path += "\\"
        return path
    return os.path.abspath(os.path.join( os.path.dirname( sys.argv[0]) , "..", ".."))


def etcDir():
    return os.path.join( emergeRoot(), "etc")

def etcPortageDir():
    """the etc directory for portage"""
    return os.path.join( etcDir(), "portage" )

class EmergeConfig( object ):
    def __init__( self ):
        self.args = None
        self._config = None
        iniPath = os.path.join( etcDir(), "kdesettings.ini" )
        if os.path.exists( iniPath ):
            self._config = configparser.ConfigParser( )
            self._config.optionxform = str
            self._config.read( iniPath )
            clean = False
            #replace possible vatiables within a section
            patern = re.compile("\${.*}")
            while not clean:
                clean = True
                for section in self._config.keys():
                    for key in self._config[section]:
                        val = self._config[section][key]
                        if patern.match(val):
                            clean = False
                            match = patern.findall(val)[0]
                            self._config[section][key] = val.replace(match, self._config[section][match[2:-1]])

    def __contains__( self, key ):
        return self._config and self._config.has_section( key[ 0 ] ) and key[ 1 ] in self._config[ key[ 0 ] ]

    def get( self, group, key, default = "_INVALID" ):
        if self.__contains__( (group, key) ):
            return self._config[ group ][ key ]
        if default != "_INVALID":
            return default
        self._config[ group ][ key ]

    def set( self, group, key, value ):
        self._config[ group ][ key ] = value


    def setDefault( self, group, key, value ):
        if not self.contains( group, key ):
            self.set( group, key, value )


emergeSettings = EmergeConfig( )


