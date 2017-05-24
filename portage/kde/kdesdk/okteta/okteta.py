import info
from CraftConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues()

        self.shortDescription = "KDE hex editor for viewing and editing the raw data of files."
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.dependencies["libs/qtbase"] = "default"
        self.dependencies["frameworks/kbookmarks"] = "default"
        self.dependencies["frameworks/kcodecs"] = "default"
        self.dependencies["frameworks/kcompletion"] = "default"
        self.dependencies["frameworks/kconfigwidgets"] = "default"
        self.dependencies["frameworks/kdbusaddons"] = "default"
        self.dependencies["frameworks/kdoctools"] = "default"
        self.dependencies["frameworks/ki18n"] = "default"
        self.dependencies["frameworks/kcmutils"] = "default"
        self.dependencies["frameworks/kio"] = "default"
        self.dependencies["frameworks/knewstuff"] = "default"
        self.dependencies["frameworks/kparts"] = "default"
        self.dependencies["frameworks/kservice"] = "default"
        self.dependencies["frameworks/kwidgetsaddons"] = "default"
        self.dependencies["frameworks/kxmlgui"] = "default"
        #self.dependencies["kdesupport/qca"] = 'default'

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
        self.defines["productname"] = "Okteta"
        self.defines["executable"] = "bin\\okteta.exe"
        #self.defines["icon"] = os.path.join(self.packageDir(), "okular.ico")

        self.ignoredPackages.append("binary/mysql-pkg")
        self.ignoredPackages.append("gnuwin32/sed")
        self.ignoredPackages.append("frameworks/kdesignerplugin")
        self.ignoredPackages.append("frameworks/kemoticons")
        self.ignoredPackages.append("kdesupport/qca")

        return TypePackager.createPackage(self)


    def preArchive(self):
        archiveDir = self.archiveDir()

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
