import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )

        self.shortDescription = "Parallelized query system"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies['kde/kconfig'] = "default"
        self.dependencies['kde/kcoreaddons'] = "default"
        self.dependencies['kde/ki18n'] = "default"
        self.dependencies['kde/kio'] = "default"
        self.dependencies['kde/kservice'] = "default"
        self.dependencies['kde/plasma'] = "default"
        self.dependencies['kde/solid'] = "default"
        self.dependencies['kde/threadweaver'] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

