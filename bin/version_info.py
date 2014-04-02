# -*- coding: utf-8 -*-
# this package contains functions to easily set versions for packages like qt5 or kde
# copyright:
# Patrick von Reth <vonreth [AT] kde [DOT] org>

import configparser
import os
import utils

_VERSION_INFOS = dict()

class VersionInfo(object):
    def __init__( self):
        self._package = None
        self._defaulVersions = None
        
    def __getVersionConfig(self, name):
        global _VERSION_INFOS
        if name in _VERSION_INFOS:
            return _VERSION_INFOS[name]
        root = os.path.dirname(name)
        dirs = [os.path.join( root, "version.ini"), os.path.join( root, "..", "version.ini")]
        
        for iniPath in dirs:
            if os.path.exists( iniPath ):
                config = configparser.ConfigParser()
                config.read(iniPath)
                _VERSION_INFOS[name] = config
                return config
        _VERSION_INFOS[name] = None
        
        
    def setupDefaultVersions(self, filename):
        self._defaulVersions = self.__getVersionConfig(filename)        
        self._package = utils.packageSplit(os.path.basename(filename))[0]
        
        
        
    def _getVersionInfo(self,key, name = ""):
        if self._defaulVersions == None:
            info = key
            if info  == None:
                info = name
            utils.fail("Please calls setupDefaultVersions(__file__) before calling self.%s()" % info)
        if self._defaulVersions.has_section("General") and key in self._defaulVersions["General"]:
                return self._defaulVersions["General"][key]
        return ""
        
    def tags(self):
        return self._getVersionInfo("tags").split(";")
        
    def branches(self):
        return self._getVersionInfo("branches").split(";")
        
    def tarballs(self):
        return self._getVersionInfo("tarballs").split(";")
        
    def defaultTarget(self):
        return self._getVersionInfo("defaulttarget")
        
    def packageName(self):
        self._getVersionInfo("","packageName")
        return self._package
        
    