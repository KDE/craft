import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.2.3'] = "ftp://ftp.gnutls.org/gcrypt/gnutls/w32/gnutls-3.2.3-w32.zip"
        self.targetDigests['3.2.3'] = '5199ab554dddbf8de4bee71bac1da3e0d4650fa1'

        self.shortDescription = "The GNU Transport Layer Security Library"
        self.defaultTarget = '3.2.3'
    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = ""
        self.subinfo.options.merge.ignoreBuildType = True

