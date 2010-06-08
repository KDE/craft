from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['1.2.3-2']:
            self.targets[ version ] = repoUrl + """/zlib-""" + version + """-bin.zip
                                """ + repoUrl + """/zlib-""" + version + """-lib.zip"""
        self.targetDigests['1.2.3-2'] = ['9858eb8f17ebc714d2f66b1a3118341a7d01b3fe',
                                         'cfc5dfef71162a6240ea0a8f8f8eed63fe82a882']
        self.defaultTarget = '1.2.3-2'

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
