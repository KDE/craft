import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )


    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["frameworks/kconfig"] = 'default'
        self.dependencies["frameworks/ki18n"] = 'default'
        self.dependencies["kde/kiconthemes"] = 'default'
        self.dependencies["kde/kio"] = 'default'
        self.dependencies["kde/knotifications"] = 'default'
        self.dependencies["frameworks/kwidgetsaddons"] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

