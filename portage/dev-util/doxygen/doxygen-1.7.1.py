import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['1.5.9'] = 'http://ftp.stack.nl/pub/users/dimitri/doxygen-1.5.9.windows.bin.zip'
        self.targets['1.7.1'] = 'http://ftp.stack.nl/pub/users/dimitri/doxygen-1.7.1.windows.bin.zip'
        self.defaultTarget = '1.7.1'
        # the zip file does not have a bin dir, so we have to create it  
        # This attribute is in prelimary state
        self.targetInstallPath['1.5.9'] = "bin"
        self.targetInstallPath['1.7.1'] = "bin"
        
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
