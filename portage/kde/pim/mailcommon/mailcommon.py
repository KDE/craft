import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "MailCommon library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/ki18n"] = "default"
        self.runtimeDependencies["frameworks/kcodecs"] = "default"
        self.runtimeDependencies["frameworks/kcompletion"] = "default"
        self.runtimeDependencies["frameworks/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/kitemmodels"] = "default"
        self.runtimeDependencies["frameworks/kitemviews"] = "default"
        self.runtimeDependencies["frameworks/kio"] = "default"
        self.runtimeDependencies["frameworks/ktextwidgets"] = "default"
        self.runtimeDependencies["frameworks/kwidgetsaddons"] = "default"
        self.runtimeDependencies["frameworks/kxmlgui"] = "default"
        self.runtimeDependencies["frameworks/kdbusaddons"] = "default"

        self.runtimeDependencies["kde/akonadi"] = "default"
        self.runtimeDependencies["kde/akonadi-mime"] = "default"
        self.runtimeDependencies["kde/messagelib"] = "default"
        self.runtimeDependencies["kde/kmailtransport"] = "default"
        self.runtimeDependencies["kde/mailimporter"] = "default"
        self.runtimeDependencies["kde/kmime"] = "default"
        self.runtimeDependencies["kde/pimcommon"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
