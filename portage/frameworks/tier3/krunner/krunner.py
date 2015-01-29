import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( tarballUrl = "http://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/portingAids/${PACKAGE_NAME}-${VERSION}.tar.xz",
                                           tarballDigestUrl = "http://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/portingAids/${PACKAGE_NAME}-${VERSION}.tar.xz.sha1")

        self.shortDescription = "Parallelized query system"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies['frameworks/kconfig'] = "default"
        self.dependencies['frameworks/kcoreaddons'] = "default"
        self.dependencies['frameworks/ki18n'] = "default"
        self.dependencies['frameworks/kio'] = "default"
        self.dependencies['frameworks/kservice'] = "default"
        self.dependencies['frameworks/plasma-framework'] = "default"
        self.dependencies['frameworks/solid'] = "default"
        self.dependencies['frameworks/threadweaver'] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

