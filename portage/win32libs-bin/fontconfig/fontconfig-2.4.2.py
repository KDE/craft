# -*- coding: utf-8 -*-
from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        self.targetDigests['2.4.2-3-vc90-bin'] = '1b7c2171fb60669924c9d7174fc2e39161f7ef7b'
        self.targetDigests['2.4.2-3-vc90-lib'] = 'e48d8c535cd245bfcc617590d3142035c77b8aa2'
        
        for version in ['2.4.2-3']:
            self.targets[ version ] = self.getPackage( repoUrl, "fontconfig", version )
            self.targetDigests[version] = self.packageDigests("fontconfig", version)

        self.defaultTarget = '2.4.2-3'

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'
        self.hardDependencies['kdesupport/kdewin'] = 'default'
        self.hardDependencies['win32libs-bin/freetype'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
