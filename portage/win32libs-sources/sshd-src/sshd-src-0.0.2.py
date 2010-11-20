# -*- coding: utf-8 -*-
import info
import utils
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.0.2'] = "http://officespace.kdab.com/~andy/CESSH-14454.zip"
        self.targetInstSrc['0.0.2'] = "SSH"
        self.patchToApply['0.0.2'] = ( 'SSH-20100512.diff', 1 )
        self.defaultTarget = '0.0.2'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/openssl'] = 'default'
        self.dependencies['win32libs-bin/zlib'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
