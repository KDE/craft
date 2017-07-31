import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(
            tarballUrl="http://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/portingAids/${PACKAGE_NAME}-${VERSION}.tar.xz",
            tarballDigestUrl="http://download.kde.org/stable/frameworks/${VERSION_MAJOR}.${VERSION_MINOR}/portingAids/${PACKAGE_NAME}-${VERSION}.tar.xz.sha1")

        self.shortDescription = "KHTML APIs"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["win32libs/giflib"] = "default"
        self.runtimeDependencies["win32libs/libjpeg-turbo"] = "default"
        self.runtimeDependencies["win32libs/libpng"] = "default"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/karchive"] = "default"
        self.runtimeDependencies["frameworks/kcodecs"] = "default"
        self.runtimeDependencies["frameworks/kglobalaccel"] = "default"
        self.runtimeDependencies["frameworks/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/ki18n"] = "default"
        self.runtimeDependencies["frameworks/kio"] = "default"
        self.runtimeDependencies["frameworks/kjs"] = "default"
        self.runtimeDependencies["frameworks/knotifications"] = "default"
        self.runtimeDependencies["frameworks/kparts"] = "default"
        self.runtimeDependencies["frameworks/ktextwidgets"] = "default"
        self.runtimeDependencies["frameworks/kwallet"] = "default"
        self.runtimeDependencies["frameworks/kwidgetsaddons"] = "default"
        self.runtimeDependencies["frameworks/sonnet"] = "default"
        self.runtimeDependencies["frameworks/kxmlgui"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
