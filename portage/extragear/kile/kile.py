import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = '[git]kde:kile'
        self.svnTargets['gitStable-2.1'] = '[git]kde:kile|2.1|'
        for ver in ['2.1.1', '2.1b5']:
            self.targets[ver] = 'http://downloads.sourceforge.net/kile/kile-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'kile-' + ver
        self.description = "a user friendly TeX/LaTeX editor for KDE"
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies['kde/kde-runtime'] = 'default'
        # this is only a dependency for kile > 2.1, but we keep it like that for now
        self.runtimeDependencies['qt-libs/poppler'] = 'default'
        # this is only a dependency for kile > 2.1, but we keep it like that for now
        self.runtimeDependencies['kde/applications/okular'] = 'default'
        self.runtimeDependencies["kde/applications/kate"] = "default"
        self.runtimeDependencies["frameworks/tier3/khtml"] = "default"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), 'blacklist.txt')
        ]

    def createPackage(self):
        self.defines["productname"] = "Kile"
        self.defines["executable"] = "bin\\kile.exe"

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()
        # TODO: Why is that needed?
        os.mkdir(os.path.join(archiveDir, "etc", "dbus-1", "session.d"))

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
