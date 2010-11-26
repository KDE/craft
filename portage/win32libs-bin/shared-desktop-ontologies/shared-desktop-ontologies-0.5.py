from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['0.1', '0.2', '0.3', '0.5']:
            self.targets[ version ] = repoUrl + """/shared-desktop-ontologies-""" + version + """-bin.tar.bz2"""
        self.targetDigests['0.5'] = '05995ee758f1bf7303d3753c94e4244b72ff3a4e'
            
        self.defaultTarget = '0.5'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
