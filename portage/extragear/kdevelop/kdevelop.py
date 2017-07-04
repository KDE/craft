import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ '5.0' ] = '[git]kde:kdevelop|5.0'
        self.svnTargets[ '5.1' ] = '[git]kde:kdevelop|5.1'
        self.svnTargets[ 'master' ] = '[git]kde:kdevelop|master'
        self.defaultTarget = '5.1'

    def setDependencies( self ):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["dev-util/zip"] = "default"
        self.runtimeDependencies["libs/qtbase"] = "default"
        self.runtimeDependencies["libs/qtdeclarative"] = "default"
        self.runtimeDependencies["libs/qtwebkit"] = "default"
        self.runtimeDependencies[ 'frameworks/karchive' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kconfig' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kguiaddons' ] = 'default'
        self.runtimeDependencies[ 'frameworks/ki18n' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kiconthemes' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kinit' ] = 'default' # runtime dep
        self.runtimeDependencies[ 'frameworks/kitemmodels' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kitemviews' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kjobwidgets' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kcmutils' ] = 'default'
        self.runtimeDependencies[ 'frameworks/knewstuff' ] = 'default'
        self.runtimeDependencies[ 'frameworks/knotifyconfig' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kparts' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kservice' ] = 'default'
        self.runtimeDependencies[ 'frameworks/sonnet' ] = 'default'
        self.runtimeDependencies[ 'frameworks/ktexteditor' ] = 'default'
        self.runtimeDependencies[ 'frameworks/threadweaver' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kwindowsystem' ] = 'default'
        self.runtimeDependencies[ 'frameworks/kxmlgui' ] = 'default'
        self.runtimeDependencies[ 'kde/libkomparediff2' ] = 'default'
        self.runtimeDependencies[ 'data/hicolor-icon-theme'] = "default"
        self.runtimeDependencies[ 'win32libs/clang'] = "default"
        if self.options.features.fullplasma:
            self.runtimeDependencies[ 'frameworks/krunner' ] = 'default'
            self.runtimeDependencies[ 'frameworks/plasma-framework' ] = 'default'
        self.runtimeDependencies[ 'extragear/kdevplatform' ] = 'default'
        self.runtimeDependencies[ 'extragear/kdevelop-pg-qt' ] = 'default'

        # Install extra plugins shipped by Kate
        self.runtimeDependencies[ 'kde/kate' ] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self):
        CMakePackageBase.__init__( self )
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(os.path.dirname(__file__), 'blacklist.txt')
        ]

    def createPackage(self):
        self.defines[ "productname" ] = "KDevelop"
        self.defines[ "website" ] = "https://kdevelop.org"
        self.defines[ "executable" ] = "bin\\kdevelop.exe"
        self.defines[ "icon" ] = os.path.join(os.path.dirname(__file__), "kdevelop.ico")
        self.defines[ "extrashortcuts" ] = r'CreateShortCut \"${startmenu}\KDevelop - Microsoft Visual C++ compiler.lnk\" \"$INSTDIR\\bin\\kdevelop-msvc.bat\"'

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()
        # TODO: Why is that needed?
        os.mkdir(os.path.join(archiveDir, "etc", "dbus-1", "session.d"))

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
