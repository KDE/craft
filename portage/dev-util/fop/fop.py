import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['1.0'] = 'http://apache.parentingamerica.com/xmlgraphics/fop/binaries/fop-1.0-bin.zip'
        self.targetDigests['1.0'] = 'afef3bbfed5543c92bc9ed2d7651422580f98bd9'
        self.targetMergeSourcePath['1.0'] = 'fop-1.0'
        self.targetInstallPath['1.0'] = "dev-utils/bin"
        self.defaultTarget = '1.0'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)

