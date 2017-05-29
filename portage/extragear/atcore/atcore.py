import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'master' ] = '[git]kde:atcore|master'
        self.defaultTarget = 'master'
        self.shortDescription = "the KDE core of Atelier Printer Host"

    def setDependencies( self ):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["libs/qtserialport"] = "default"
        self.dependencies["libs/qtcharts"] = "default"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self):
        CMakePackageBase.__init__( self )
        self.blacklist_file = [
            NSIPackagerLists.runtimeBlacklist,
            os.path.join(self.packageDir(), 'blacklist.txt')
        ]
        self.changePackager( NullsoftInstallerPackager )

    def createPackage(self):
        self.defines[ "productname" ] = "AtCoreTest"
        self.defines[ "executable" ] = "bin\\AtCoreTest.exe"
        self.defines[ "setupname" ] = "AtCore-x64.exe"
        self.defines[ "icon" ] = os.path.join(self.packageDir(), "atelier.ico")


        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()
        # TODO: Why is that needed?
        os.mkdir(os.path.join(archiveDir, "etc", "dbus-1", "session.d"))

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
