from distutils.dir_util import mkpath

import info
from Blueprints.CraftVersion import CraftVersion


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "KDE Integrated Development Environment for C/C++/QML/JS/Python/PHP/..."

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["dev-util/7zip"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = "default"
        self.runtimeDependencies["frameworks/tier1/breeze-icons"] = "default"
        self.runtimeDependencies["frameworks/tier1/karchive"] = "default"
        self.runtimeDependencies["frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["frameworks/tier1/kguiaddons"] = "default"
        self.runtimeDependencies["frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["frameworks/tier3/kinit"] = "default"
        self.runtimeDependencies["frameworks/tier1/kitemmodels"] = "default"
        self.runtimeDependencies["frameworks/tier1/kitemviews"] = "default"
        self.runtimeDependencies["frameworks/tier2/kjobwidgets"] = "default"
        self.runtimeDependencies["frameworks/tier3/kcmutils"] = "default"
        self.runtimeDependencies["frameworks/tier3/knewstuff"] = "default"
        self.runtimeDependencies["frameworks/tier3/knotifyconfig"] = "default"
        self.runtimeDependencies["frameworks/tier3/kparts"] = "default"
        self.runtimeDependencies["frameworks/tier3/kservice"] = "default"
        self.runtimeDependencies["frameworks/tier1/sonnet"] = "default"
        self.runtimeDependencies["frameworks/tier3/ktexteditor"] = "default"
        self.runtimeDependencies["frameworks/tier1/threadweaver"] = "default"
        self.runtimeDependencies["frameworks/tier1/kwindowsystem"] = "default"
        self.runtimeDependencies["frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["kde/kdesdk/libkomparediff2"] = "default"
        self.runtimeDependencies["data/hicolor-icon-theme"] = "default"
        self.runtimeDependencies["win32libs/llvm-meta/clang"] = "default"

        # handle kdevplatform merge into kdevelop.git
        if self.buildTarget != "master" and CraftVersion(self.buildTarget) < CraftVersion("5.2"):
            self.runtimeDependencies["extragear/kdevelop/kdevplatform"] = "default"
        else:
            self.runtimeDependencies["libs/qt5/qtquickcontrols"] = "default"
            self.runtimeDependencies["libs/qt5/qtwebengine"] = "default"
            self.runtimeDependencies["kdesupport/grantlee"] = "default"

        if self.options.features.fullplasma:
            self.runtimeDependencies["frameworks/tier3/krunner"] = "default"
            self.runtimeDependencies["frameworks/tier3/plasma-framework"] = "default"
        if self.options.features.fullkdevelop:
            self.runtimeDependencies["extragear/kdevelop/kdev-python"] = "default"
            self.runtimeDependencies["extragear/kdevelop/kdev-php"] = "default"
        self.runtimeDependencies["extragear/kdevelop-pg-qt"] = "default"

        # Install extra plugins shipped by Kate
        self.runtimeDependencies["kde/applications/kate"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file.append(os.path.join(os.path.dirname(__file__), 'blacklist.txt'))

    def createPackage(self):
        self.defines["productname"] = "KDevelop"
        self.defines["website"] = "https://kdevelop.org"
        self.defines["executable"] = "bin\\kdevelop.exe"
        self.defines["icon"] = os.path.join(os.path.dirname(__file__), "kdevelop.ico")
        self.defines["extrashortcuts"] = 'CreateShortCut "${startmenu}\\KDevelop - Microsoft Visual C++ compiler.lnk" "$INSTDIR\\bin\\kdevelop-msvc.bat"'

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)

    def preArchive(self):
        archiveDir = self.archiveDir()
        # TODO: Why is that needed?
        mkpath(os.path.join(archiveDir, "etc", "dbus-1", "session.d"))

        # TODO: Just blacklisting this doesn't work. WTF?
        utils.rmtree(os.path.join(archiveDir, "dev-utils"))
