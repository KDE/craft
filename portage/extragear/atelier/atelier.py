import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'master' ] = '[git]kde:atelier|master'
        self.defaultTarget = 'master'
        self.shortDescription = 'Atelier Printer Host'

    def setDependencies( self ):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["frameworks/kxmlgui"] = "default"
        self.buildDependencies["frameworks/solid"] = "default"
        self.buildDependencies["frameworks/kconfigwidgets"] = "default"
        self.buildDependencies["frameworks/ktexteditor"] = "default"
        self.buildDependencies["frameworks/ki18n"] = "default"
        self.buildDependencies["extragear/atcore"] = "default"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["libs/qtserialport"] = "default"
        self.runtimeDependencies["libs/qtcharts"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(self.packageDir(), 'blacklist.txt')
        ]

    def createPackage(self):
        self.defines[ "productname" ] = "Atelier"
        self.defines[ "executable" ] = "bin\\atelier.exe"
        self.defines[ "setupname" ] = "Atelier-x64.exe"
        self.defines[ "version" ] = "1.0"
        self.defines[ "website" ] = "https://atelier.kde.org"
        self.defines[ "icon" ] = os.path.join(self.packageDir(), "atelier.ico")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()
        # TODO: Why is that needed?
        os.mkdir(os.path.join(archiveDir, "etc", "dbus-1", "session.d"))

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
