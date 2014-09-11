import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KService provides a plugin framework for handling desktop services."

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["kde/kconfig"] = "default"
        self.dependencies["kde/kcoreaddons"] = "default"
        self.dependencies["kde/kcrash"] = "default"
        self.dependencies["kde/kdbusaddons"] = "default"
        self.dependencies["kde/ki18n"] = "default"
        self.dependencies["kde/kdoctools"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

