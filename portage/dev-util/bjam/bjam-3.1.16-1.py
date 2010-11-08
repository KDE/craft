# -*- coding: iso-8859-15 -*-
import base
import info
import os
import shutil
import utils

PACKAGE_NAME         = "boost-jam"
PACKAGE_VER          = "3.1.18"
PACKAGE_FULL_VER     = "3.1.18-1"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_FULL_VER)

SRC_URI= """
http://downloads.sourceforge.net/boost/""" + PACKAGE_FULL_NAME + """-ntx86.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[PACKAGE_FULL_VER ] = SRC_URI
        self.targetInstSrc[PACKAGE_FULL_VER ] = PACKAGE_FULL_NAME + "-ntx86"
        self.defaultTarget = PACKAGE_FULL_VER 

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True        
        self.subinfo.options.merge.destinationPath = "dev-utils";
        BinaryPackageBase.__init__(self)
    
    def unpack(self):
        if not BinaryPackageBase.unpack(self):
            return False
        return utils.renameDir(os.path.join(self.imageDir(),PACKAGE_FULL_NAME + "-ntx86"),os.path.join(self.imageDir(),'bin')) 
        return True

if __name__ == '__main__':
    Package().execute()
