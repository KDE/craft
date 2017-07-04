import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ 'master' ] = '[git]kde:peruse|master'
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies[ 'libs/qtbase' ] = "default"
        self.runtimeDependencies[ 'frameworks/karchive' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kconfig' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kdeclarative' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kfilemetadata' ] = 'default'
        self.runtimeDependencies[ 'frameworks/ki18n' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kiconthemes' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kio' ] = 'default'
        self.runtimeDependencies[ 'frameworks/plasma-framework' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kirigami' ] = 'default'
        self.runtimeDependencies[ 'kde/okular' ] = 'default'
        self.runtimeDependencies[ 'kde/kio-extras' ] = 'default'
        self.runtimeDependencies[ 'frameworks/knewstuff' ] = 'default'
        self.runtimeDependencies[ 'frameworks/breeze-icons' ] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self):
        CMakePackageBase.__init__( self )
        self.subinfo.options.fetch.checkoutSubmodules = True
        whitelists = []
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), 'blacklist.txt')
        ]

    def createPackage(self):
        self.defines[ "productname" ] = "Peruse Comic Book Viewer"
        self.defines[ "executable" ] = "bin\\peruse.exe"
        self.defines[ "website" ] = "http://peruse.kde.org"
        self.defines[ "icon" ] = os.path.join(os.path.dirname(__file__), "peruse.ico")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()
        # TODO: Why is that needed?
        os.mkdir(os.path.join(archiveDir, "etc", "dbus-1", "session.d"))

        # TODO: Can we generalize this for other apps?
        # move everything to the location where Qt expects it
        binPath = os.path.join(archiveDir, "bin")

        utils.moveFile(os.path.join(archiveDir, "etc", "xdg", "peruse.knsrc"), os.path.join(binPath, "data", "peruse.knsrc"))

        utils.mergeTree(os.path.join(archiveDir, "lib", "qca-qt5"), binPath)

        utils.rmtree(os.path.join(self.archiveDir(),"lib"))

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))

        return True
