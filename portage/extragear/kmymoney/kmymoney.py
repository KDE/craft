import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['master'] = '[git]kde:kmymoney|master'
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.dependencies['frameworks/karchive'] = 'default'
        self.dependencies["frameworks/kconfig"] = 'default'
        self.dependencies["frameworks/kconfigwidgets"] = 'default'
        self.dependencies["frameworks/ki18n"] = 'default'
        self.dependencies['frameworks/khtml'] = 'default'
        self.dependencies["frameworks/kcompletion"] = 'default'
        self.dependencies['frameworks/kcmutils'] = 'default'
        self.dependencies["frameworks/kiconthemes"] = 'default'
        self.dependencies["frameworks/kio"] = 'default'
        self.dependencies["frameworks/kitemmodels"] = 'default'
        self.dependencies["frameworks/kitemviews"] = 'default'
        self.dependencies["frameworks/kservice"] = 'default'
        self.dependencies["frameworks/kwallet"] = 'default'
        self.dependencies["frameworks/knotifications"] = 'default'
        self.dependencies["frameworks/kxmlgui"] = 'default'
        self.dependencies["frameworks/ktextwidgets"] = 'default'
        #self.dependencies['testing/gpgmepp'] = 'default'
        self.dependencies['kde/kholidays'] = 'default'
        self.dependencies['binary/mysql-pkg'] = 'default'
        self.dependencies['win32libs/sqlite'] = 'default'
        #self.dependencies['win32libs/libofx'] = 'default'
        self.dependencies['win32libs/gettext'] = 'default'
        self.dependencies['extragear/libalkimia'] = 'default'
        self.dependencies['extragear/kdiagram'] = 'default'
        self.buildDependencies['dev-util/gettext-tools'] = 'default'
        self.shortDescription = "a personal finance manager for KDE"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self):
        CMakePackageBase.__init__( self )
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), 'blacklist.txt')
        ]

    def createPackage(self):
        self.defines[ "productname" ] = "KMyMoney"
        self.defines[ "executable" ] = "bin\\kmymoney.exe"
        self.defines[ "icon" ] = os.path.join(os.path.dirname(__file__), "kmymoney.ico")

        self.ignoredPackages.append("binary/mysql-pkg")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()
        # TODO: Why is that needed?
        os.mkdir(os.path.join(archiveDir, "etc", "dbus-1", "session.d"))

        # TODO: Can we generalize this for other apps?
        # move everything to the location where Qt expects it
        binPath = os.path.join(archiveDir, "bin")

        utils.mergeTree(os.path.join(archiveDir, "lib", "plugins"), binPath)
        utils.mergeTree(os.path.join(archiveDir, "lib", "qml"), os.path.join(archiveDir, binPath))

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
        return TypePackager.preArchive(self)
