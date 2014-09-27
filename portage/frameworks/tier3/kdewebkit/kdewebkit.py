import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KDE Integration for QtWebKit"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
#        self.dependencies['libs/qtwebkit-widgets'] = "default"
        self.dependencies['frameworks/kconfig'] = "default"
        self.dependencies['frameworks/kcoreaddons'] = "default"
        self.dependencies['frameworks/kio'] = "default"
        self.dependencies['frameworks/kjobwidgets'] = "default"
        self.dependencies['frameworks/kparts'] = "default"
        self.dependencies['frameworks/kservice'] = "default"
        self.dependencies['frameworks/kwallet'] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

