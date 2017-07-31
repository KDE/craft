import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "KEditBookmarks"
        self.patchToApply['17.04.1'] = [("fix_keditbookmarks_unistd.patch", 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "master"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["frameworks/kcoreaddons"] = "default"
        self.runtimeDependencies["frameworks/ki18n"] = "default"
        self.runtimeDependencies["frameworks/kio"] = "default"
        self.runtimeDependencies["frameworks/kbookmarks"] = "default"
        self.runtimeDependencies["frameworks/kparts"] = "default"
        self.runtimeDependencies["frameworks/kwindowsystem"] = "default"
        self.runtimeDependencies["frameworks/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/kdoctools"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
