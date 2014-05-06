import info
from EmergeConfig import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultVersions("http://download.kde.org/unstable/frameworks/${VERSION}/${PACKAGE_NAME}-${VERSION}.tar.xz",
                                            "http://download.kde.org/unstable/frameworks/${VERSION}/${PACKAGE_NAME}-${VERSION}.tar.xz.sha1",
                                            "${PACKAGE_NAME}-${VERSION}",
                                            "[git]kde:${PACKAGE_NAME}" )

        self.shortDescription = "the KDE text editor"
        self.defaultTarget = 'frameworks'

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["libs/qtbase"] = "default"
        self.dependencies["kde/kconfigwidgets"] = "default"
        self.dependencies["kde/kdoctools"] = "default"
        self.dependencies["kde/kguiaddons"] = "default"
        self.dependencies["kde/ki18n"] = "default"
        self.dependencies["kde/kinit"] = "default"
        self.dependencies["kde/kjobwidgets"] = "default"
        self.dependencies["kde/kio"] = "default"
        self.dependencies["kde/kparts"] = "default"
        self.dependencies["kde/ktexteditor"] = "default"
        self.dependencies["kde/kwindowsystem"] = "default"
        self.dependencies["kde/kxmlgui"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF "
