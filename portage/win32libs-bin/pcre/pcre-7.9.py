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
            self.targetDigests['7.9'] = ['42950ad7c207aaf18856cee6b16763889c69f164',
                                         'ebe08572bd0ab22499d0cd4a620bbd06df4d25ab']
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
