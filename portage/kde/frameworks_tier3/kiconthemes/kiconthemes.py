import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultVersions("http://download.kde.org/unstable/frameworks/${VERSION}/${PACKAGE_NAME}-${VERSION}.tar.xz",
                                            "http://download.kde.org/unstable/frameworks/${VERSION}/${PACKAGE_NAME}-${VERSION}.tar.xz.sha1",
                                            "${PACKAGE_NAME}-${VERSION}",
                                            "[git]kde:${PACKAGE_NAME}" )

        self.shortDescription = "Classes to improve the handling of icons"
        

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["libs/qtdbus"] = "default"
        self.dependencies["libs/qtsvg"] = "default"
        self.dependencies["kde/ki18n"] = "default"
        self.dependencies["kde/kconfigwidgets"] = "default"
        self.dependencies["kde/kwidgetsaddons"] = "default"
        self.dependencies["kde/kitemviews"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

