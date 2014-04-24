# -*- coding: utf-8 -*-
# copyright:
# Patrick von Reth <vonreth [AT] kde [DOT] org>

import configparser
import os
import sys


def emergeRoot():
    return os.path.abspath(os.path.join( os.path.dirname( sys.argv[0]) , "..", ".."))


def etcDir():
    return os.path.join( emergeRoot(), "etc")

def etcPortageDir():
    """the etc directory for portage"""
    return os.path.join( etcDir(), "portage" )

class EmergeConfig( object ):
    def __init__( self ):
        self.args = None
        self.config = None
        iniPath = os.path.join( etcDir(), "kdesettings.ini" )
        if os.path.exists( iniPath ):
            self.config = configparser.ConfigParser( )
            self.config.optionxform = str
            self.config.read( iniPath )

    def __contains__( self, key ):
        return self.config and self.config.has_section( key[ 0 ] ) and key[ 1 ] in self.config[ key[ 0 ] ]

    def get( self, group, key, default = None ):
        if self.__contains__( (group, key) ):
            return self.config[ group ][ key ]
        if default != None:
            return default
        self.config[ group ][ key ]

    def set( self, group, key, value ):
        self.config[ group ][ key ] = value


    def setDefault( self, group, key, value ):
        if not self.contains( group, key ):
            self.set( group, key, value )


emergeSettings = EmergeConfig( )


