import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultVersions("http://download.kde.org/unstable/frameworks/${VERSION}/${PACKAGE_NAME}-${VERSION}.tar.xz",
                                            "http://download.kde.org/unstable/frameworks/${VERSION}/${PACKAGE_NAME}-${VERSION}.tar.xz.sha1",
                                            "${PACKAGE_NAME}-${VERSION}",
                                            "[git]kde:${PACKAGE_NAME}" )

        self.shortDescription = "TODO"
        

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["win32libs/automoc"] = "default"
        self.dependencies["kde/kconfig"] = "default"
        self.dependencies["kde/kcoreaddons"] = "default"
        self.dependencies["kde/kdbusaddons"] = "default"
        self.dependencies["kde/ki18n"] = "default"
        self.dependencies["kde/kiconthemes"] = "default"
        self.dependencies["win32libs/gcrypt"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

