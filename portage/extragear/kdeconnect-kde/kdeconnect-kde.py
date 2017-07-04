import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['master'] = '[git]kde:kdeconnect-kde'
        self.defaultTarget = 'master'
        self.shortDescription = "KDE Connect adds communication between KDE and your smartphone"

    def setDependencies( self ):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies['libs/qtbase'] = 'default'
        self.runtimeDependencies['kdesupport/qca'] = 'default'
        self.runtimeDependencies['frameworks/ki18n'] = 'default'
        self.runtimeDependencies['frameworks/kconfigwidgets'] = 'default'
        self.runtimeDependencies['frameworks/kdbusaddons'] = 'default'
        self.runtimeDependencies['frameworks/kiconthemes'] = 'default'
        self.runtimeDependencies['frameworks/knotifications'] = 'default'
        self.runtimeDependencies['frameworks/kcmutils'] = 'default'
        self.runtimeDependencies[ 'frameworks/breeze-icons' ] = 'default'

class Package( CMakePackageBase ):
    def __init__( self):
        CMakePackageBase.__init__( self )
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), "blacklist.txt")
        ]

    def createPackage(self):
        self.defines[ "productname" ] = "KDE Connect"
        self.defines[ "executable" ] = "bin\\kdeconnect-indicator.exe"
        self.defines[ "icon" ] = os.path.join(os.path.dirname(__file__), "icon.ico")

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()

        # move everything to the location where Qt expects it
        binPath = os.path.join(archiveDir, "bin")
        utils.mergeTree(os.path.join(archiveDir, "lib/qca-qt5"), binPath)

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))

