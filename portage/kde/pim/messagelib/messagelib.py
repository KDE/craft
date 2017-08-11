import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Messagelib library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["frameworks/tier1/karchive"] = "default"
        self.runtimeDependencies["frameworks/tier2/kcompletion"] = "default"
        self.runtimeDependencies["frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/tier1/kitemviews"] = "default"
        self.runtimeDependencies["frameworks/tier2/kjobwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["frameworks/tier3/kservice"] = "default"
        self.runtimeDependencies["frameworks/tier1/sonnet"] = "default"
        self.runtimeDependencies["frameworks/tier3/ktextwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier1/kwidgetsaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/kwindowsystem"] = "default"
        self.runtimeDependencies["frameworks/tier1/syntax-highlighting"] = "default"
        self.runtimeDependencies["frameworks/tier1/ki18n"] = "default"

        self.runtimeDependencies["kde/pim/kmime"] = "default"
        self.runtimeDependencies["kde/pim/akonadi"] = "default"
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = "default"
        self.runtimeDependencies["kde/pim/akonadi-mime"] = "default"
        self.runtimeDependencies["kde/pim/grantleetheme"] = "default"
        self.runtimeDependencies["kde/pim/kmailtransport"] = "default"
        self.runtimeDependencies["kde/pim/kmbox"] = "default"
        self.runtimeDependencies["kde/pim/pimcommon"] = "default"
        self.runtimeDependencies["kde/pim/kldap"] = "default"
        self.runtimeDependencies["kdesupport/grantlee"] = "default"
        self.runtimeDependencies["win32libs/libxslt"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebengine"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
