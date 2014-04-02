# -*- coding: utf-8 -*-
# copyright:
# Patrick von Reth <vonreth [AT] kde [DOT] org>

import configparser
import os
import utils


emergeSettings = None

class EmergeConfig(object):
    def __init__(self):
        self.config = None
        iniPath = os.path.join(os.getenv("KDEROOT"), "etc", "kdesettings.ini")
        if os.path.exists(iniPath):
            self.config = configparser.ConfigParser()
            self.config.optionxform = str
            self.config.read(iniPath)
            
    
    def contains(self, group, key):
        # print("[%s] = %s " % (group, key))
        return self.config and self.config.has_section( group ) and key in self.config[ group ]
        
    def get(self, group, key):
        if self.contains(group,key):
            return self.config[ group ][ key ]
        return None
    


    
if emergeSettings == None:
    emergeSettings = EmergeConfig()