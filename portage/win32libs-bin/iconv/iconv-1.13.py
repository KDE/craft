from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['1.12', '1.12-1', '1.13', '1.13-2']:
            self.targets[ version ] = repoUrl + """/iconv-""" + version + """-bin.tar.bz2
                                """ + repoUrl + """/iconv-""" + version + """-lib.tar.bz2"""

        self.targetDigests['1.13-2'] = ['88c02623292d5e40fc908b0be7f90da53cf49c6b',
                                        'ce91f1105699b7cb67d71fab597efb3d4f178b83']
        self.defaultTarget = '1.13-2'

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
