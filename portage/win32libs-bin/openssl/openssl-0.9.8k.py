# -*- coding: utf-8 -*-
from Package.BinaryPackageBase import *
import os
import info
import platform

class subinfo(info.infoclass):
    def setTargets( self ):
        for version in [ '0.9.8j-1', '0.9.8k-3', '1.0.0' ]:
            self.targets[ version ] = self.getUnifiedPackage( 'http://downloads.sourceforge.net/kde-windows' , "openssl" , version )
            
        if platform.buildArchitecture() == 'x64' and COMPILER == "mingw4":
            self.defaultTarget = '1.0.0'
        else:
            self.defaultTarget = '0.9.8k-3'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
