import info
from Package.CMakePackageBase import *
from Packager.NullsoftInstallerPackager import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.shortDescription = "KolourPaint is an easy-to-use paint program"
        self.svnTargets['master'] = "[git]kde:kolourpaint|frameworks"

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.dependencies['kdesupport/qimageblitz'] = 'default'
        self.buildDependencies["dev-util/extra-cmake-modules"] = "default"
        self.buildDependencies["libs/qtbase"] = "default"
        self.dependencies["frameworks/kconfig"] = "default"
        self.dependencies["frameworks/kdoctools"] = "default"
        self.dependencies["frameworks/kguiaddons"] = "default"
        self.dependencies["frameworks/kdelibs4support"] = "default"
        self.dependencies["frameworks/ki18n"] = "default"
        self.dependencies["frameworks/kinit"] = "default"
        self.dependencies["frameworks/kjobwidgets"] = "default"
        self.dependencies["frameworks/kio"] = "default"
        self.dependencies["frameworks/kparts"] = "default"
        self.dependencies["frameworks/ktexteditor"] = "default"
        self.dependencies["frameworks/kwindowsystem"] = "default"
        self.dependencies["frameworks/kxmlgui"] = "default"
        self.dependencies["frameworks/kdbusaddons"] = "default"
        self.dependencies["frameworks/threadweaver"] = "default"

class Package( CMakePackageBase, NullsoftInstallerPackager ):
    def __init__( self):
        CMakePackageBase.__init__( self )
        blacklists = [
            NSIPackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), 'blacklist.txt')
        ]
        NullsoftInstallerPackager.__init__(self, blacklists=blacklists)

    def createPackage(self):
        self.defines[ "productname" ] = "Kolourpaint"
        self.defines[ "executable" ] = "bin\\kolourpaint.exe"
        self.defines[ "icon" ] = os.path.join(os.path.dirname(__file__), "icon.ico")

        self.ignoredPackages.append("binary/mysql-pkg")

        return NullsoftInstallerPackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()

        # TODO: Can we generalize this for other apps?
        # move everything to the location where Qt expects it
        binPath = os.path.join(archiveDir, "bin")

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))

