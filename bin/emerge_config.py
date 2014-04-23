# -*- coding: utf-8 -*-
# copyright:
# Patrick von Reth <vonreth [AT] kde [DOT] org>

import configparser
import os

import utils


class EmergeConfig(object):
    def __init__(self):
        self.args = None
        self.config = None
        iniPath = os.path.join(os.getenv("KDEROOT"), "etc", "kdesettings.ini")
        if os.path.exists(iniPath):
            self.config = configparser.ConfigParser()
            self.config.optionxform = str
            self.config.read(iniPath)
            
    def __contains__(self, key):
        if len(key) != 2:
            utils.die("Wrong key %s" % key)
        return self.config and self.config.has_section( key[0] ) and key[1] in self.config[ key[0] ]
        
    def get(self, group, key, default = None):
        if self.__contains__((group,key)):
            return self.config[ group ][ key ]
        if default != None:
            return default
        self.config[ group ][ key ]
        utils.die("unknown key %s/%s" % ( group , key))
        
    def set(self, group, key , value):
        self.config[ group ][ key ] = value
        
        
    def setDefault(self, group, key , value):
        if not self.contains( group, key ):
            self.set(group, key, value)
    




emergeSettings = EmergeConfig()