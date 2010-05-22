import info
import platform

class subinfo( info.infoclass ):
    def setTargets( self ):
        arch = "x86"
        if platform.buildArchitecture() == "x64":
		  arch = "x64"
        self.targets['2.2'] = 'http://www.dependencywalker.com/depends22_'+arch+'.zip'
        self.defaultTarget = '2.2'
        # the zip file does not have a bin dir, so we have to create it  
        # This attribute is in prelimary state
        self.targetInstallPath['2.2'] = "bin"
        
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
