import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['1.5.9', '1.7.1', '1.7.3', '1.7.4', '1.8.1.2', '1.8.2', '1.8.3.1', '1.8.4', '1.8.5']:
            self.targets[ ver ] = 'ftp://ftp.stack.nl/pub/users/dimitri/doxygen-%s.windows.bin.zip' % ver
            self.targetInstallPath[ ver ] = "bin"
            
        self.targetDigests['1.7.1'] = '29d2a80444300e5de383fb79bf096d2af05c55ce'
        self.targetDigests['1.7.3'] = '9dfe3c48f674900fba7537a47706feb6a1bed528'
        self.targetDigests['1.7.4'] = 'd3e869a5c04796115c5121911ac5f371481ba7f6'
        self.targetDigests['1.8.2'] = '95eb9882ea105435556c92d71acb19150fd6c76b'
        self.targetDigests['1.8.4'] = 'e12c1eb90de5800a0dc0124c855b7e51c622e7be'
        self.targetDigests['1.8.5'] = '2102a49c05b36b1ca945c433eaf02845b7ea895c'

        self.shortDescription = 'Automated C, C++, and Java Documentation Generator'
        self.defaultTarget = '1.8.5'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
