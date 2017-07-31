import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.shortDescription = 'a desktop planetarium'
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies['libs/qtbase'] = 'default'
        self.runtimeDependencies['libs/qtdeclarative'] = 'default'
        self.runtimeDependencies['libs/qtquickcontrols'] = 'default'
        self.runtimeDependencies['libs/qtquickcontrols2'] = 'default'
        self.runtimeDependencies['libs/qtsvg'] = 'default'
        self.runtimeDependencies['frameworks/kconfig'] = 'default'
        self.runtimeDependencies['frameworks/kdoctools'] = 'default'
        self.runtimeDependencies['frameworks/kwidgetsaddons'] = 'default'
        self.runtimeDependencies['frameworks/knewstuff'] = 'default'
        self.runtimeDependencies['frameworks/kdbusaddons'] = 'default'
        self.runtimeDependencies['frameworks/ki18n'] = 'default'
        self.runtimeDependencies['frameworks/kinit'] = 'default'
        self.runtimeDependencies['frameworks/kjobwidgets'] = 'default'
        self.runtimeDependencies['frameworks/kio'] = 'default'
        self.runtimeDependencies['frameworks/kxmlgui'] = 'default'
        self.runtimeDependencies['frameworks/kplotting'] = 'default'
        self.runtimeDependencies['frameworks/knotifications'] = 'default'
        self.runtimeDependencies['frameworks/knotifyconfig'] = 'default'
        self.runtimeDependencies['win32libs/eigen3'] = 'default'
        self.runtimeDependencies['win32libs/cfitsio'] = 'default'
        self.runtimeDependencies['win32libs/wcslib'] = 'default'
        self.runtimeDependencies['win32libs/indiclient'] = 'default'
        self.runtimeDependencies['win32libs/libraw'] = 'default'
        self.runtimeDependencies['win32libs/gsl'] = 'default'

        # Install proper theme
        self.runtimeDependencies['frameworks/breeze-icons'] = 'default'


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file = [PackagerLists.runtimeBlacklist, os.path.join(self.packageDir(), 'blacklist.txt')]

    def createPackage(self):
        self.defines["productname"] = "KStars Desktop Planetarium"
        self.defines["executable"] = "bin\\kstars.exe"
        self.defines["icon"] = os.path.join(self.packageDir(), "kstars.ico")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()
        # TODO: Why is that needed?
        os.mkdir(os.path.join(archiveDir, "etc", "dbus-1", "session.d"))

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
