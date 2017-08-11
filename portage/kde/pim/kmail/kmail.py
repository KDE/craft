import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KMail"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["frameworks/tier1/kcodecs"] = "default"
        self.runtimeDependencies["frameworks/tier2/kcompletion"] = "default"
        self.runtimeDependencies["frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["frameworks/tier2/kcrash"] = "default"
        self.runtimeDependencies["frameworks/tier1/kdbusaddons"] = "default"
        self.runtimeDependencies["frameworks/tier2/kdoctools"] = "default"
        self.runtimeDependencies["frameworks/tier1/kguiaddons"] = "default"
        self.runtimeDependencies["frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["frameworks/tier3/kcmutils"] = "default"
        self.runtimeDependencies["frameworks/tier3/knotifyconfig"] = "default"
        self.runtimeDependencies["frameworks/tier3/kparts"] = "default"
        self.runtimeDependencies["frameworks/tier1/sonnet"] = "default"
        self.runtimeDependencies["frameworks/tier3/kservice"] = "default"
        self.runtimeDependencies["frameworks/tier3/ktextwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier1/kwidgetsaddons"] = "default"
        self.runtimeDependencies["frameworks/tier3/kxmlgui"] = "default"

        self.runtimeDependencies["kde/pim/kmime"] = "default"
        self.runtimeDependencies["kde/pim/akonadi"] = "default"
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = "default"
        self.runtimeDependencies["kde/pim/akonadi-mime"] = "default"
        self.runtimeDependencies["kde/pim/kpimtextedit"] = "default"
        self.runtimeDependencies["kde/pim/kimap"] = "default"
        self.runtimeDependencies["kdesupport/grantlee"] = "default"
        self.runtimeDependencies["kde/pim/kldap"] = "default"
        self.runtimeDependencies["kde/pim/kcalcore"] = "default"
        self.runtimeDependencies["kde/pim/kcalutils"] = "default"
        self.runtimeDependencies["kde/pim/kidentitymanagement"] = "default"
        self.runtimeDependencies["kde/pim/kmailtransport"] = "default"
        self.runtimeDependencies["kde/pim/messagelib"] = "default"
        self.runtimeDependencies["kde/pim/ktnef"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebengine"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
