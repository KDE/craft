import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KRuler app"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["libs/qt5/qtbase"] = "default"
        self.buildDependencies["frameworks/tier2/kdoctools"] = "default"
        self.buildDependencies["frameworks/tier1/ki18n"] = "default"
        self.buildDependencies["frameworks/tier3/knotifications"] = "default"
        self.buildDependencies["frameworks/tier1/kwindowsystem"] = "default"
        self.buildDependencies["frameworks/tier3/kxmlgui"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
