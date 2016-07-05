import info
from EmergeConfig import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "GpgME++ is a C++ wrapper (or C++ bindings) for the GnuPG project's gpgme (GnuPG Made Easy) library, version 0.4.4 and later."

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["libs/qtbase"] = "default"
        self.dependencies["win32libs/gpgme"] = "default"
        self.dependencies["win32libs/boost"] = "default"
        
from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
