import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KDE Integration for QtWebKit"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies['libs/qtwebkit'] = "default"
        self.runtimeDependencies['frameworks/kconfig'] = "default"
        self.runtimeDependencies['frameworks/kcoreaddons'] = "default"
        self.runtimeDependencies['frameworks/kio'] = "default"
        self.runtimeDependencies['frameworks/kjobwidgets'] = "default"
        self.runtimeDependencies['frameworks/kparts'] = "default"
        self.runtimeDependencies['frameworks/kservice'] = "default"
        self.runtimeDependencies['frameworks/kwallet'] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

