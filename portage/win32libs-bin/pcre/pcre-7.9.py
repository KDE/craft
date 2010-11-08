# -*- coding: utf-8 -*-
from Package.BinaryPackageBase import *
import os
import info
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['7.8','7.9', '8.02']:
            self.targets[ version ] = self.getPackage( repoUrl, "pcre", version )
        self.defaultTarget = '7.9'

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
