import info


SRC_URI = """
http://www.winkde.org/pub/kde/ports/win32/repository/gnuwin32/findutils-4.2.20-2-bin.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['4.2.20-2'] = SRC_URI
        self.defaultTarget = '4.2.20-2'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)
        #  manifest file from package is empty -> add a switch to force manifest generating 
        self.forceCreateManifestFiles = True

if __name__ == '__main__':
    Package().execute()
