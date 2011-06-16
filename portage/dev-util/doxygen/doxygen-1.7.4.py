import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['1.5.9'] = 'http://ftp.stack.nl/pub/users/dimitri/doxygen-1.5.9.windows.bin.zip'
        self.targets['1.7.1'] = 'http://ftp.stack.nl/pub/users/dimitri/doxygen-1.7.1.windows.bin.zip'
        self.targets['1.7.3'] = 'http://ftp.stack.nl/pub/users/dimitri/doxygen-1.7.3.windows.bin.zip'
        self.targets['1.7.4'] = 'http://ftp.stack.nl/pub/users/dimitri/doxygen-1.7.4.windows.bin.zip'
        self.targetDigests['1.7.1'] = '29d2a80444300e5de383fb79bf096d2af05c55ce'
        self.targetDigests['1.7.3'] = '9dfe3c48f674900fba7537a47706feb6a1bed528'
        self.targetDigests['1.7.4'] = 'd3e869a5c04796115c5121911ac5f371481ba7f6'
        self.defaultTarget = '1.7.4'
        # the zip file does not have a bin dir, so we have to create it
        # This attribute is in prelimary state
        self.targetInstallPath['1.5.9'] = "bin"
        self.targetInstallPath['1.7.1'] = "bin"
        self.targetInstallPath['1.7.3'] = "bin"
        self.targetInstallPath['1.7.4'] = "bin"

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
