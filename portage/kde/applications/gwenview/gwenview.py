import info
from EmergeConfig import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Gwenview is a fast and easy to use image viewer for KDE."

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["libs/qtbase"] = "default"
        self.dependencies["win32libs/libjpeg-turbo"] = "default"
        self.dependencies["win32libs/libpng"] = "default"
        self.dependencies["win32libs/exiv2"] = "default"
        self.dependencies["win32libs/lcms2"] = "default"
        self.dependencies["frameworks/libkdcraw"] = "default"
        self.dependencies["frameworks/kactivities"] = "default"
        self.dependencies["frameworks/kdelibs4support"] = "default"
        self.dependencies["qt-libs/phonon"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
