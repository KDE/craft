# -*- coding: utf-8 -*-
from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for ver in ['0.10.3', '0.10.4', '0.10.5', '0.10.6', '0.12.0', '0.12.2']:
            self.targets[ ver ] = self.getPackage( repoUrl, "poppler", ver )

        self.defaultTarget = '0.12.2'

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'
        self.hardDependencies['win32libs-bin/fontconfig'] = 'default'
        self.hardDependencies['win32libs-bin/freetype'] = 'default'
        self.hardDependencies['win32libs-bin/openjpeg'] = 'default'
        self.hardDependencies['win32libs-bin/lcms'] = 'default'
        self.hardDependencies['win32libs-bin/jpeg'] = 'default'
        self.hardDependencies['data/poppler-data'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
