import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.svnTargets['frameworks'] = '[git]kde:libkexiv2|frameworks'
        self.defaultTarget = 'frameworks'
        
        self.shortDescription = "Libkexiv2 is a wrapper around Exiv2 library to manipulate pictures metadata as EXIF IPTC and XMP."

    def setDependencies( self ):
        self.dependencies['win32libs/exiv2'] = 'default'
        self.dependencies['frameworks/extra-cmake-modules'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )

