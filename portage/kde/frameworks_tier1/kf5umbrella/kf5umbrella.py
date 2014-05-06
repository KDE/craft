import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "KF5 Umbrella"
        

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["win32libs/automoc"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

