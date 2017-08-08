import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = '[git]kde:kmymoney|master'
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["frameworks/tier1/karchive"] = "default"
        self.runtimeDependencies["frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["frameworks/tier3/kconfigwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["frameworks/tier3/khtml"] = "default"
        self.runtimeDependencies["frameworks/tier2/kcompletion"] = "default"
        self.runtimeDependencies["frameworks/tier3/kcmutils"] = "default"
        self.runtimeDependencies["frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["frameworks/tier1/kitemmodels"] = "default"
        self.runtimeDependencies["frameworks/tier1/kitemviews"] = "default"
        self.runtimeDependencies["frameworks/tier3/kservice"] = "default"
        self.runtimeDependencies["frameworks/tier3/kwallet"] = "default"
        self.runtimeDependencies["frameworks/tier3/knotifications"] = "default"
        self.runtimeDependencies["frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["frameworks/tier3/ktextwidgets"] = "default"
        # self.runtimeDependencies['testing/gpgmepp'] = 'default'
        self.runtimeDependencies["kde/pim/kholidays"] = "default"
        self.runtimeDependencies["binary/mysql"] = "default"
        self.runtimeDependencies["win32libs/sqlite"] = "default"
        # self.runtimeDependencies["win32libs/libofx"] = "default"
        self.runtimeDependencies["win32libs/gettext"] = "default"
        self.runtimeDependencies["extragear/libalkimia"] = "default"
        self.runtimeDependencies["extragear/kdiagram"] = "default"
        self.buildDependencies["dev-util/gettext-tools"] = "default"
        self.description = "a personal finance manager for KDE"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), 'blacklist.txt')
        ]

    def createPackage(self):
        self.defines["productname"] = "KMyMoney"
        self.defines["executable"] = "bin\\kmymoney.exe"
        self.defines["icon"] = os.path.join(os.path.dirname(__file__), "kmymoney.ico")

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()
        # TODO: Why is that needed?
        os.mkdir(os.path.join(archiveDir, "etc", "dbus-1", "session.d"))

        # TODO: Can we generalize this for other apps?
        # move everything to the location where Qt expects it
        binPath = os.path.join(archiveDir, "bin")

        utils.mergeTree(os.path.join(archiveDir, "lib", "plugins"), binPath)
        utils.mergeTree(os.path.join(archiveDir, "lib", "qml"), os.path.join(archiveDir, binPath))

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
        return TypePackager.preArchive(self)
