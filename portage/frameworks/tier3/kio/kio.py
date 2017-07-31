import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "Network transparent access to files and data"

        self.patchToApply['5.31.0'] = ('0001-Fix-double-export-in-already-exported-class.patch', 1)

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["frameworks/karchive"] = "default"
        self.runtimeDependencies["frameworks/kbookmarks"] = "default"
        self.runtimeDependencies["frameworks/kcodecs"] = "default"
        self.runtimeDependencies["frameworks/kcompletion"] = "default"
        self.runtimeDependencies["frameworks/kconfig"] = "default"
        self.runtimeDependencies["frameworks/kconfigwidgets"] = "default"
        self.runtimeDependencies["frameworks/kcoreaddons"] = "default"
        self.runtimeDependencies["frameworks/kdbusaddons"] = "default"
        self.runtimeDependencies["frameworks/kdoctools"] = "default"
        self.runtimeDependencies["frameworks/ki18n"] = "default"
        self.runtimeDependencies["frameworks/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/kitemviews"] = "default"
        self.runtimeDependencies["frameworks/kjobwidgets"] = "default"
        self.runtimeDependencies["frameworks/knotifications"] = "default"
        self.runtimeDependencies["frameworks/kservice"] = "default"
        self.runtimeDependencies["frameworks/solid"] = "default"
        self.runtimeDependencies["frameworks/kwidgetsaddons"] = "default"
        self.runtimeDependencies["frameworks/kwindowsystem"] = "default"
        self.runtimeDependencies["frameworks/kxmlgui"] = "default"
        self.runtimeDependencies["frameworks/kwallet"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        if OsUtils.isWin() or OsUtils.isMac():
            self.subinfo.options.configure.args = " -DKIO_FORK_SLAVES=ON "
