import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Process launcher to speed up launching KDE applications"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["frameworks/kconfig"] = "default"
        self.dependencies["frameworks/kcrash"] = "default"
        self.dependencies["frameworks/kdoctools"] = "default"
        self.dependencies["frameworks/ki18n"] = "default"
        self.dependencies["frameworks/kio"] = "default"
        self.dependencies["frameworks/kservice"] = "default"
        self.dependencies["frameworks/kwindowsystem"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
