from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['1.2.34', '1.2.35']:
            self.targets[ version ] = repoUrl + """/libpng-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/libpng-""" + version + """-lib.tar.bz2"""

        self.targetDigests['1.2.35'] = ['6a55cf096f990168396c79f329084b149dc819fe',
                                        '29f8b950e4f6971f6eee20424fe27bf66b171e1b']            
        self.defaultTarget = '1.2.35'

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
