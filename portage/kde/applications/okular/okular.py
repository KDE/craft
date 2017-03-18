import info
from CraftConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.shortDescription = "KDE document viewer"

    def setDependencies( self ):
        self.buildDependencies['win32libs/chm'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['qt-libs/poppler'] = 'default'
        self.dependencies['win32libs/tiff'] = 'default'
        self.dependencies['win32libs/djvu'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.dependencies['win32libs/freetype'] = 'default'
        self.dependencies['win32libs/ebook-tools'] = 'default'
        self.buildDependencies['win32libs/libspectre'] = 'default'
        self.dependencies['win32libs/ghostscript'] = 'default'
        self.dependencies['kde/libkexiv2'] = 'default'
        self.dependencies['frameworks/karchive'] = 'default'
        self.dependencies['frameworks/kbookmarks'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kconfigwidgets'] = 'default'
        self.dependencies['frameworks/kcoreaddons'] = 'default'
        self.dependencies['frameworks/kdbusaddons'] = 'default'
        self.dependencies['frameworks/kjs'] = 'default'
        self.dependencies['frameworks/kio'] = 'default'
        self.dependencies['frameworks/kparts'] = 'default'
        self.dependencies['frameworks/threadweaver'] = 'default'
        self.dependencies['frameworks/kwallet'] = 'default'
        self.dependencies['frameworks/khtml'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), "blacklist.txt")
        ]
        self.changePackager(NullsoftInstallerPackager)


    def createPackage(self):
        self.defines["productname"] = "Okular"
        self.defines["executable"] = "bin\\okular.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "okular.ico")

        self.ignoredPackages.append("binary/mysql-pkg")
        self.ignoredPackages.append("gnuwin32/sed")
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
