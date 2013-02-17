import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['1.5.9', '1.7.1', '1.7.3', '1.7.4', '1.8.2', '1.8.3.1']:
            self.targets[ ver ] = 'http://ftp.stack.nl/pub/users/dimitri/doxygen-%s.windows.bin.zip' % ver
            self.targetInstallPath[ ver ] = "bin"
            
        self.targetDigests['1.7.1'] = '29d2a80444300e5de383fb79bf096d2af05c55ce'
        self.targetDigests['1.7.3'] = '9dfe3c48f674900fba7537a47706feb6a1bed528'
        self.targetDigests['1.7.4'] = 'd3e869a5c04796115c5121911ac5f371481ba7f6'
        self.targetDigests['1.8.2'] = '95eb9882ea105435556c92d71acb19150fd6c76b'
        self.defaultTarget = '1.8.3.1'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
