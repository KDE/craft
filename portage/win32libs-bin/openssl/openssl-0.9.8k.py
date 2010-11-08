# -*- coding: utf-8 -*-
from Package.BinaryPackageBase import *
import os
import info
import emergePlatform

class subinfo(info.infoclass):
    def setTargets( self ):
        for version in [ '0.9.8j-1', '0.9.8k-3', '1.0.0' ]:
            self.targets[ version ] = self.getUnifiedPackage( 'http://downloads.sourceforge.net/kde-windows' , "openssl" , version )
        
        self.targetDigests['0.9.8k-3'] = ['0c451b00d2a3691f58f2997b95afcde8511bbd1b',
                                          'ac3b1517d9c0e1132f18909caeab0d9b804e1406']
            
        if emergePlatform.buildArchitecture() == 'x64' and COMPILER == "mingw4":
            self.defaultTarget = '1.0.0'
        else:
            self.defaultTarget = '0.9.8k-3'

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True
        

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
