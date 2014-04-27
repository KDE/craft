import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '2011-08' ] =  "http://www.ldraw.org/library/updates/complete.zip"
        self.targetDigests['2011-08'] = '8c6b62f9385bdcd288f249340e713d8e3c6adba7'
        self.shortDescription = 'LDraw Parts Library'
        self.defaultTarget = '2011-08'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        BinaryPackageBase.__init__( self )
        self.subinfo.options.install.installPath = "share"

