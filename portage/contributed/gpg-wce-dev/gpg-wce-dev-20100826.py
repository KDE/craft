from Package.BinaryPackageBase import *
import os
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['latest'] = \
                """http://files.kolab.org/local/windows-ce/gpg_wince-dev-latest.zip"""
        self.targetDigests['20100823'] = "34a922ac947e90828cae9ad471ca6ae56495b1dd"
        self.targets['20100823'] = \
                """http://files.kolab.org/local/windows-ce/gpg_wince-dev-230810.zip"""
        self.targetDigests['20100826'] = "ff6c1d6b0ac663e08cba28ac96d1f7e17c223da1"
        self.targets['20100826'] = \
                """http://files.kolab.org/local/windows-ce/gpg_wince-dev-260810.zip"""
        self.defaultTarget = '20100826'

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
