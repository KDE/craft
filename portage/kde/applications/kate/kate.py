import info
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "the KDE text editor"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["frameworks/tier2/kdoctools"] = "default"
        self.runtimeDependencies["frameworks/tier1/kguiaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["frameworks/tier3/kinit"] = "default"
        self.runtimeDependencies["frameworks/tier2/kjobwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["frameworks/tier3/kparts"] = "default"
        self.runtimeDependencies["frameworks/tier3/ktexteditor"] = "default"
        self.runtimeDependencies["frameworks/tier1/kwindowsystem"] = "default"
        self.runtimeDependencies["frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["frameworks/tier1/kdbusaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/kitemmodels"] = "default"
        self.runtimeDependencies["frameworks/tier3/kactivities"] = "default"
        if self.options.features.fullplasma:
            self.runtimeDependencies["frameworks/tier3/plasma-framework"] = "default"
        self.runtimeDependencies["frameworks/tier1/threadweaver"] = "default"
        self.runtimeDependencies["frameworks/tier3/knewstuff"] = "default"
        if OsUtils.isUnix():
            self.runtimeDependencies["kde/applications/konsole"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file.append(os.path.join(os.path.dirname(__file__), 'blacklist.txt'))

    def createPackage(self):
        self.defines["productname"] = "Kate"
        self.defines["executable"] = "bin\\kate.exe"
        self.defines["icon"] = os.path.join(os.path.dirname(__file__), "kate.ico")

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()
        # TODO: Why is that needed?
        os.mkdir(os.path.join(archiveDir, "etc", "dbus-1", "session.d"))

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
