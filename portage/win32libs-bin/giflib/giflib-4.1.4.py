from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['4.1.4-1']:
            self.targets[ version ] = repoUrl + """/giflib-""" + version + """-bin.zip
                                """ + repoUrl + """/giflib-""" + version + """-lib.zip"""

        self.targetDigests['4.1.4-1'] = ['8bb64ce3e75513c6bf2e799d41278121cb7fc33e',
                                         'fbbac3488180eb91850d7a09f38cee1c66ee79c8']            
        self.defaultTarget = '4.1.4-1'

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
