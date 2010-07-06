from Package.BinaryPackageBase import *
import os
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '20100706' ] = """http://files.kolab.org/local/windows-ce/gpg_wince-dev-latest.zip"""
        self.defaultTarget = '20100706'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )
    
if __name__ == '__main__':
    Package().execute()
