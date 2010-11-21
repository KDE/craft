# -*- coding: iso-8859-15 -*-
import base
import info
import os
import shutil
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['3.1.18-1']:
          name = "boost-jam-%s-ntx86" % ver
          self.targets[ ver ] = "http://downloads.sourceforge.net/boost/%s.zip" % name
          self.targetInstSrc[ ver ] = name
        self.targetDigests['3.1.18-1'] = 'c26094ec2f93978076e475f50c5c9f828e8d6463'

        self.defaultTarget = '3.1.18-1'

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
        return utils.renameDir(self.sourceDir(),os.path.join(self.imageDir(),'bin')) 
        return True

if __name__ == '__main__':
    Package().execute()
