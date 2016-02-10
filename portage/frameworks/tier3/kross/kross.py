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
        self.dependencies['libs/qttools'] = "default"
        self.dependencies['frameworks/kcompletion'] = "default"
        self.dependencies['frameworks/kcoreaddons'] = "default"
        self.dependencies['frameworks/kdoctools'] = "default"
        self.dependencies['frameworks/ki18n'] = "default"
        self.dependencies['frameworks/kiconthemes'] = "default"
        self.dependencies['frameworks/kio'] = "default"
        self.dependencies['frameworks/kparts'] = "default"
        self.dependencies['frameworks/kservice'] = "default"
        self.dependencies['frameworks/kwidgetsaddons'] = "default"
        self.dependencies['frameworks/kxmlgui'] = "default"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )


    

