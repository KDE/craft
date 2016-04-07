import info
from Packager.NullsoftInstallerPackager import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'master' ] = '[git]kde:peruse|master'
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies[ 'frameworks/karchive' ] = 'default'
        self.dependencies[ 'frameworks/kconfig' ] = 'default'
        self.dependencies[ 'frameworks/kdeclarative' ] = 'default'
        self.dependencies[ 'frameworks/kfilemetadata' ] = 'default'
        self.dependencies[ 'frameworks/ki18n' ] = 'default'
        self.dependencies[ 'frameworks/kiconthemes' ] = 'default'
        self.dependencies[ 'frameworks/kio' ] = 'default'
        self.dependencies[ 'data/hicolor-icon-theme'] = "default"
        self.dependencies[ 'frameworks/plasma-framework' ] = 'default'
        self.dependencies[ 'testing/kirigami' ] = 'default'
        self.dependencies[ 'kde/okular' ] = 'default'

        # Install proper theme
        self.dependencies[ 'frameworks/oxygen-icons5' ] = 'default'
        self.dependencies[ 'frameworks/breeze-icons' ] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase, NullsoftInstallerPackager ):
    def __init__( self):
        CMakePackageBase.__init__( self )
        self.subinfo.options.fetch.checkoutSubmodules = True
        blacklists = [
            NSIPackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), 'blacklist.txt')
        ]
        NullsoftInstallerPackager.__init__(self, blacklists=blacklists)

    def createPackage(self):
        self.defines[ "productname" ] = "Peruse Comic Book Viewer"
        self.defines[ "executable" ] = "bin\\peruse.exe"
        self.defines[ "icon" ] = os.path.join(os.path.dirname(__file__), "peruse.ico")

        return NullsoftInstallerPackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()
        # TODO: Why is that needed?
        os.mkdir(os.path.join(archiveDir, "etc", "dbus-1", "session.d"))

        # TODO: Can we generalize this for other apps?
        # move everything to the location where Qt expects it
        binPath = os.path.join(archiveDir, "bin")

        utils.mergeTree(os.path.join(archiveDir, "plugins"), binPath)
        utils.mergeTree(os.path.join(archiveDir, "lib", "plugins"), binPath)
        utils.mergeTree(os.path.join(archiveDir, "qml"), os.path.join(archiveDir, binPath))
        utils.mergeTree(os.path.join(archiveDir, "lib", "qml"), os.path.join(archiveDir, binPath))

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
