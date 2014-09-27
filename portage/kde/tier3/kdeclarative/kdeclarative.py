import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Provides integration of QML and KDE Frameworks"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies['kde/kconfig'] = 'default'
        self.dependencies['kde/ki18n'] = 'default'
        self.dependencies['kde/kiconthemes'] = 'default'
        self.dependencies['kde/kio'] = 'default'
        self.dependencies['frameworks/kwidgetsaddons'] = 'default'
        self.dependencies['kde/kwindowsystem'] = 'default'
        self.dependencies['kde/kglobalaccel'] = 'default'
        self.dependencies['kde/kguiaddons'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

