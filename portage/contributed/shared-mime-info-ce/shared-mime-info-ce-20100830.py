from Package.BinaryPackageBase import *
import os
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.01'] = \
                """http://officespace.kdab.com/~andy/shared-mime-info-ce.zip"""
        #self.targetDigests['20100823'] = "34a922ac947e90828cae9ad471ca6ae56495b1dd"
        self.defaultTarget = '0.01'

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
