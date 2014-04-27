import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['2.8'] = 'http://download.sysinternals.com/Files/ProcessMonitor.zip'
        self.defaultTarget = '2.8'
        # the zip file does not have a bin dir, so we have to create it
        # This attribute is in prelimary state
        self.targetInstallPath['2.8'] = "bin"

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "dev-utils"
        self.subinfo.options.merge.ignoreBuildType = True

