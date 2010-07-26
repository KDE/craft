# -*- coding: utf-8 -*-
from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for ver in ['0.18', '0.18.1', '0.18.2', '0.19']:
            self.targets[ ver ] = self.getPackage( repoUrl, "exiv2", ver )

        ## @todo url's returned from self.getPackage are compiler specific, hard coded digests does not work yet
        self.targetDigests['0.19'] = ['c253b2b463fe62cc552028b26a21ed4bad6096bf',
                                      '7d6b5c2003e32c980b7bb64dfd8dd9942a46e5e6']
        self.defaultTarget = '0.19'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['win32libs-bin/expat'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
