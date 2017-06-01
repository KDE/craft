import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "A barcode abstraction layer providing uniform access to generation of barcodes with data"


    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.buildDependencies["win32libs/libqrencode"] = "default"
        self.buildDependencies["win32libs/libdmtx"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
