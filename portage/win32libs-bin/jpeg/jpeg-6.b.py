from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['6.b-5']:
            self.targets[ version ] = repoUrl + """/jpeg-""" + version + """-bin.zip
                                """ + repoUrl + """/jpeg-""" + version + """-lib.zip"""
        
        self.targetDigests['6.b-5'] = ['098a653a9432932c03b92923654be85ab4d1d026',
                                       '38c3b7cc28ed70e06f361f37bb63974790792bdb']
        self.defaultTarget = '6.b-5'

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
