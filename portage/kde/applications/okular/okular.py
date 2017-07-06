import info
from CraftConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.shortDescription = "KDE document viewer"

    def setDependencies( self ):
        self.buildDependencies['win32libs/chm'] = 'default'
        self.runtimeDependencies['libs/qtbase'] = 'default'
        self.runtimeDependencies['qt-libs/poppler'] = 'default'
        self.runtimeDependencies['win32libs/tiff'] = 'default'
        self.runtimeDependencies['win32libs/djvu'] = 'default'
        self.runtimeDependencies['win32libs/zlib'] = 'default'
        self.runtimeDependencies['win32libs/freetype'] = 'default'
        self.runtimeDependencies['win32libs/ebook-tools'] = 'default'
        self.buildDependencies['win32libs/libspectre'] = 'default'
        self.runtimeDependencies['win32libs/ghostscript'] = 'default'
        self.runtimeDependencies['kde/libkexiv2'] = 'default'
        self.runtimeDependencies['frameworks/karchive'] = 'default'
        self.runtimeDependencies['frameworks/kbookmarks'] = 'default'
        self.runtimeDependencies['frameworks/kconfig'] = 'default'
        self.runtimeDependencies['frameworks/kconfigwidgets'] = 'default'
        self.runtimeDependencies['frameworks/kcoreaddons'] = 'default'
        self.runtimeDependencies['frameworks/kdbusaddons'] = 'default'
        self.runtimeDependencies['frameworks/kjs'] = 'default'
        self.runtimeDependencies['frameworks/kio'] = 'default'
        self.runtimeDependencies['frameworks/kparts'] = 'default'
        self.runtimeDependencies['frameworks/threadweaver'] = 'default'
        self.runtimeDependencies['frameworks/kwallet'] = 'default'
        self.runtimeDependencies['frameworks/khtml'] = 'default'
        self.runtimeDependencies['kdesupport/qca'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        CMakePackageBase.__init__( self )
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), "blacklist.txt")
        ]


    def createPackage(self):
        self.defines["productname"] = "Okular"
        self.defines["executable"] = "bin\\okular.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "okular.ico")

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("gnuwin32/sed")
        self.ignoredPackages.append("frameworks/kdesignerplugin")
        self.ignoredPackages.append("frameworks/kemoticons")

        return TypePackager.createPackage(self)


    def preArchive(self):
        archiveDir = self.archiveDir()

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
