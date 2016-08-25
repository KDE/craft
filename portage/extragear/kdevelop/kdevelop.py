import info
from Packager.NullsoftInstallerPackager import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ '5.0' ] = '[git]kde:kdevelop|5.0'
        self.defaultTarget = '5.0'

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["dev-util/zip"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["libs/qtdeclarative"] = "default"
        self.dependencies["libs/qtwebkit"] = "default"
        self.dependencies[ 'frameworks/karchive' ] = 'default'
        self.dependencies[ 'frameworks/kconfig' ] = 'default'
        self.dependencies[ 'frameworks/kguiaddons' ] = 'default'
        self.dependencies[ 'frameworks/ki18n' ] = 'default'
        self.dependencies[ 'frameworks/kiconthemes' ] = 'default'
        self.dependencies[ 'frameworks/kinit' ] = 'default' # runtime dep
        self.dependencies[ 'frameworks/kitemmodels' ] = 'default'
        self.dependencies[ 'frameworks/kitemviews' ] = 'default'
        self.dependencies[ 'frameworks/kjobwidgets' ] = 'default'
        self.dependencies[ 'frameworks/kcmutils' ] = 'default'
        self.dependencies[ 'frameworks/knewstuff' ] = 'default'
        self.dependencies[ 'frameworks/knotifyconfig' ] = 'default'
        self.dependencies[ 'frameworks/kparts' ] = 'default'
        self.dependencies[ 'frameworks/kservice' ] = 'default'
        self.dependencies[ 'frameworks/sonnet' ] = 'default'
        self.dependencies[ 'frameworks/ktexteditor' ] = 'default'
        self.dependencies[ 'frameworks/threadweaver' ] = 'default'
        self.dependencies[ 'frameworks/kwindowsystem' ] = 'default'
        self.dependencies[ 'frameworks/kxmlgui' ] = 'default'
        self.dependencies[ 'kde/libkomparediff2' ] = 'default'
        self.dependencies[ 'data/hicolor-icon-theme'] = "default"
        self.dependencies[ 'dev-util/clang'] = "default"
        if self.options.features.fullplasma:
            self.dependencies[ 'frameworks/krunner' ] = 'default'
            self.dependencies[ 'frameworks/plasma-framework' ] = 'default'
        self.dependencies[ 'extragear/kdevplatform' ] = 'default'

        # Install extra plugins shipped by Kate
        self.dependencies[ 'kde/kate' ] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self):
        CMakePackageBase.__init__( self )
        self.blacklist_file = [
            NSIPackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), 'blacklist.txt')
        ]
        self.changePackager( NullsoftInstallerPackager )

    def createPackage(self):
        self.defines[ "productname" ] = "KDevelop"
        self.defines[ "executable" ] = "bin\\kdevelop.exe"
        self.defines[ "icon" ] = os.path.join(os.path.dirname(__file__), "kdevelop.ico")

        self.ignoredPackages.append("binary/mysql-pkg")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()
        # TODO: Why is that needed?
        os.mkdir(os.path.join(archiveDir, "etc", "dbus-1", "session.d"))

        # TODO: Can we generalize this for other apps?
        # move everything to the location where Qt expects it
        binPath = os.path.join(archiveDir, "bin")

        utils.mergeTree(os.path.join(archiveDir, "plugins"), binPath)
        utils.mergeTree(os.path.join(archiveDir, "qml"), os.path.join(archiveDir, binPath))

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
