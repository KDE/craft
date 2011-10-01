from Package.BinaryPackageBase import *
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""

        for version in ['4.2.4']:
            self.targets[ version ] = self.getUnifiedPackage( repoUrl, "libgmp", version )

        self.targetDigests['4.2.4'] = ['83afa5092746dac350b40f8d823a958b688ff7d8',
                                       '34addc0e7a1d0c3e1057a0a71c79626e6c4e2dcc']

        self.defaultTarget = '4.2.4'

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
