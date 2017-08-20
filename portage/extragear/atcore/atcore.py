import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = '[git]kde:atcore|master'
        self.defaultTarget = 'master'
        self.description = "the KDE core of Atelier Printer Host"

    def setDependencies(self):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtserialport"] = "default"
        self.runtimeDependencies["libs/qt5/qtcharts"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(self.packageDir(), 'blacklist.txt')
        ]

    def createPackage(self):
        self.defines["productname"] = "AtCoreTest"
        self.defines["executable"] = "bin\\AtCoreTest.exe"
        self.defines["setupname"] = "AtCore-x64-0.1.exe"
        self.defines["version"] = "0.1"
        self.defines["website"] = "https://atelier.kde.org"
        self.defines["icon"] = os.path.join(self.packageDir(), "atcore.ico")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()
        # TODO: Why is that needed?
        os.mkdir(os.path.join(archiveDir, "etc", "dbus-1", "session.d"))

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
