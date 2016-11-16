import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.svnTargets["gitHEAD"] = "[git]kde:kolourpaint"
        self.defaultTarget = "gitHEAD"
        self.shortDescription = "KolourPaint is an easy-to-use paint program"

    def setDependencies( self ):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        #self.dependencies["libs/runtime"] = "default" #mingw-based builds need this
        self.dependencies["kde/libkexiv2"] = "default"
        self.dependencies["frameworks/kconfig"] = "default"
        self.dependencies["frameworks/kguiaddons"] = "default"
        self.dependencies["frameworks/kdelibs4support"] = "default"
        self.dependencies["frameworks/ki18n"] = "default"
        self.dependencies["frameworks/kio"] = "default"
        self.dependencies["frameworks/kparts"] = "default"
        self.dependencies["frameworks/kxmlgui"] = "default"
        self.dependencies["frameworks/breeze-icons"] = 'default'

class Package( CMakePackageBase ):
    def __init__( self):
        CMakePackageBase.__init__( self )
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), "blacklist.txt")
        ]
        self.changePackager( NullsoftInstallerPackager )

    def createPackage(self):
        self.defines[ "productname" ] = "Kolourpaint"
        self.defines[ "executable" ] = "bin\\kolourpaint.exe"
        self.defines[ "icon" ] = os.path.join(self.packageDir(), "kolourpaint.ico")

        self.ignoredPackages.append("binary/mysql-pkg")
        self.ignoredPackages.append("frameworks/kdesignerplugin")
        self.ignoredPackages.append("frameworks/kemoticons")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()

        # move everything to the location where Qt expects it
        binPath = os.path.join(archiveDir, "bin")
        utils.mergeTree(os.path.join(archiveDir, "plugins"), binPath)
        utils.mergeTree(os.path.join(archiveDir, "qml"), os.path.join(archiveDir, binPath))
        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
        return TypePackager.preArchive(self)