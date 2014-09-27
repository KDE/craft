import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Parallelized query system"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies['frameworks/kconfig'] = "default"
        self.dependencies['frameworks/kcoreaddons'] = "default"
        self.dependencies['frameworks/ki18n'] = "default"
        self.dependencies['frameworks/kio'] = "default"
        self.dependencies['frameworks/kservice'] = "default"
        self.dependencies['frameworks/plasma'] = "default"
        self.dependencies['frameworks/solid'] = "default"
        self.dependencies['frameworks/threadweaver'] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

