from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""
        
        for version in ['0.17-1']:
            self.targets[ version ] = self.getUnifiedPackage( repoUrl, "gettext", version )
        self.targetDigests['0.17-1'] = ['5c21b674addf0607ba0ec4cb8833ce2c7825dbf6',
                                        'dbf633faf50f55eed9b95b26171a2f70645e446e']
            
        self.defaultTarget = '0.17-1'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['win32libs-bin/iconv'] = 'default'

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
