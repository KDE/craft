# -*- coding: utf-8 -*-

import os;
import utils;

from PackageBase import *;

from BuildSystem.BuildSystemFactory import *;
from Source.SourceFactory import *;
from Packager.PackagerFactory import *;

class PackageMultiBase (PackageBase):
    """Provides a generic interface for packages and implements the basic stuff for all packages"""
    
    buildSystemType = None
    packagerType = None
    
    def __init__(self):
        if utils.verbose > 1:
            print "PackageMultiBase.__init__ called"
        PackageBase.__init__(self)
        
    def execute(self):
        if utils.verbose > 1:
            print "PackageMultiBase.execute called"

        self.subinfo.setBuildTarget()
        # for conventience - todo is this really required 
        self.buildTarget = self.subinfo.buildTarget
            
        self.source = SourceFactory(self.subinfo)
        self.buildSystem = BuildSystemFactory(self.buildSystemType, self.source)
        self.packager = PackagerFactory(self.packagerType, self.buildSystem)
        
        PackageBase.execute(self)
                    
    def fetch(self):
        return self.source.fetch()
        
    def unpack(self):
        return self.source.unpack()

    def configure(self):
        return self.buildSystem.configure()

    def compile(self):
        return self.buildSystem.compile()

    def make(self):
        return self.buildSystem.make()

    def install(self):
        return self.buildSystem.install()
        
    def uninstall(self):
        return self.buildSystem.uninstall()

    def createPackage(self):
        return self.packageSystem.createPackage()

    def setDirectories(self):
        self.buildSystem.subinfo = self.subinfo
        #self.packageSystem.subinfo = self.subinfo
        return self.buildSystem.setDirectories()
    