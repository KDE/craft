import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KDE Integration for QtWebKit"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
#        self.dependencies['libs/qtwebkit-widgets'] = "default"
        self.dependencies['kde/kconfig'] = "default"
        self.dependencies['kde/kcoreaddons'] = "default"
        self.dependencies['kde/kio'] = "default"
        self.dependencies['kde/kjobwidgets'] = "default"
        self.dependencies['kde/kparts'] = "default"
        self.dependencies['kde/kservice'] = "default"
        self.dependencies['kde/kwallet'] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

