import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues(
            tarballUrl = "http://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/portingAids/kross-${VERSION}.tar.xz",
            tarballDigestUrl = "http://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/portingAids/kross-${VERSION}.tar.xz.sha1"
        )

        self.shortDescription = "Multi-language application scripting"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies['libs/qttools'] = "default"
        self.runtimeDependencies['frameworks/kcompletion'] = "default"
        self.runtimeDependencies['frameworks/kcoreaddons'] = "default"
        self.runtimeDependencies['frameworks/kdoctools'] = "default"
        self.runtimeDependencies['frameworks/ki18n'] = "default"
        self.runtimeDependencies['frameworks/kiconthemes'] = "default"
        self.runtimeDependencies['frameworks/kio'] = "default"
        self.runtimeDependencies['frameworks/kparts'] = "default"
        self.runtimeDependencies['frameworks/kservice'] = "default"
        self.runtimeDependencies['frameworks/kwidgetsaddons'] = "default"
        self.runtimeDependencies['frameworks/kxmlgui'] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

