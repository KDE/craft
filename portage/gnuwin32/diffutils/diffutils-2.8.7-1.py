import info

## \todo the dep files will let into have dll's installed multiple times
SRC_URI = """
http://downloads.sourceforge.net/sourceforge/gnuwin32/diffutils-2.8.7-1-bin.zip
http://downloads.sourceforge.net/sourceforge/gnuwin32/diffutils-2.8.7-1-dep.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.8.7-1'] = SRC_URI
        self.defaultTarget = '2.8.7-1'
        self.targetDigests['2.8.7-1'] = ['892460fee6f19ff38d70872ac565fbb97f9d3c16',
                                         '426636df15901f95b0f2a57ef325e876695aaa57']

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
