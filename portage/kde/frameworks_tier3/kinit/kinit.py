import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultVersions("http://download.kde.org/unstable/frameworks/${VERSION}/${PACKAGE_NAME}-${VERSION}.tar.xz",
                                            "http://download.kde.org/unstable/frameworks/${VERSION}/${PACKAGE_NAME}-${VERSION}.tar.xz.sha1",
                                            "${PACKAGE_NAME}-${VERSION}",
                                            "[git]kde:${PACKAGE_NAME}" )

        self.shortDescription = "Process launcher to speed up launching KDE applications"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["kde/kconfig"] = "default"
        self.dependencies["kde/kcrash"] = "default"
        self.dependencies["kde/kdoctools"] = "default"
        self.dependencies["kde/ki18n"] = "default"
        self.dependencies["kde/kio"] = "default"
        self.dependencies["kde/kservice"] = "default"
        self.dependencies["kde/kwindowsystem"] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )
