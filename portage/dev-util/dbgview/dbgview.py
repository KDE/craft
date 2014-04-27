import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['4.81'] = 'http://download.sysinternals.com/files/DebugView.zip'
        self.defaultTarget = '4.81'
        # the zip file does not have a bin dir, so we have to create it
        # This attribute is in prelimary state
        self.targetInstallPath['4.81'] = "bin"

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"

