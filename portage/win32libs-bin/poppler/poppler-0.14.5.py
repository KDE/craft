# -*- coding: utf-8 -*-
from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for ver in ['0.14.0', '0.14.1', '0.14.3', '0.14.4', '0.14.5']:
            self.targets[ ver ] = self.getPackage( repoUrl, "poppler", ver )

        self.shortDescription = "PDF rendering library based on xpdf-3.0"
        self.defaultTarget = '0.14.5'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        self.dependencies['win32libs-bin/freetype'] = 'default'
        self.dependencies['win32libs-bin/openjpeg'] = 'default'
        self.dependencies['win32libs-bin/lcms'] = 'default'
        self.dependencies['win32libs-bin/zlib'] = 'default'
        self.dependencies['win32libs-bin/jpeg'] = 'default'
        self.dependencies['win32libs-bin/libpng'] = 'default'
        self.dependencies['win32libs-bin/libxml2'] = 'default'
        self.runtimeDependencies['data/poppler-data'] = 'default'
        self.dependencies['libs/qt'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
