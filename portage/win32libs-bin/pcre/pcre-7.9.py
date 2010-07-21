# -*- coding: utf-8 -*-
from Package.BinaryPackageBase import *
import os
import info
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['7.8','7.9']:
            self.targets[ version ] = self.getPackage( repoUrl, "pcre", version )
        if compiler.isMSVC():
            self.targetDigests['7.9'] = ['eea9c07409dbb0fb048bb2f699b62265cc98a90a',
                                         '4ae2a3ae0ba493a630c25879a7201d153314e9c4']
        if compiler.isMinGW():
            self.targetDigests['7.9'] = ['85ad8e9ccaa3d3fcab072338eb8640fdbe16809e',
                                         'd84f74784693e38c86fa750806068374453f9f60']
        self.defaultTarget = '7.9'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True
        

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
