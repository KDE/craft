import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "TODO"
        

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["frameworks/kconfig"] = "default"
        self.dependencies["frameworks/kcoreaddons"] = "default"
        self.dependencies["frameworks/kdbusaddons"] = "default"
        self.dependencies["frameworks/ki18n"] = "default"
        self.dependencies["frameworks/kiconthemes"] = "default"
        self.dependencies["frameworks/knotifications"] = "default"
        self.dependencies["frameworks/kwindowsystem"] = "default"
        self.dependencies["win32libs/gcrypt"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

