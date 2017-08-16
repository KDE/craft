import glob

import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/KDAB/GammaRay.git"
        for ver in ["2.7.0"]:
            self.targets[ver] = f"https://github.com/KDAB/GammaRay/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"GammaRay-{ver}"
            self.archiveNames[ver] = f"gammaray-{ver}.tar.gz"
        self.targetDigests['2.7.0'] = (
            ['74251d9de4bfa31994431c7a493e5de17d0b90853557a245bf3f7f4e0227fd14'], CraftHash.HashAlgorithm.SHA256)

        self.description = "GammaRay is a tool to poke around in a Qt-application and also to manipulate the application to some extent"

        self.defaultTarget = "2.7.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["frameworks/tier1/syntax-highlighting"] = "default"
        self.runtimeDependencies["qt-apps/kdstatemachineeditor"] = "default"
        self.runtimeDependencies["win32libs/openssl"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DGAMMARAY_INSTALL_QT_LAYOUT=ON -DGAMMARAY_BUILD_DOCS=OFF"
        if not craftSettings.getboolean("QtSDK", "Enabled", False):
            self.subinfo.options.configure.args += " -DGAMMARAY_MULTI_BUILD=OFF"
        if self.subinfo.options.dynamic.gammarayProbeOnly:
            self.subinfo.options.configure.args += " -DGAMMARAY_BUILD_UI=OFF"
            self.changePackager(SevenZipPackager)
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            lambda: (re.compile(r"^.*\.pdb$|^.*\.pri$|^share.*$|^etc.*$"),)
        ]

    def preArchive(self):
        if self.buildType() == "Debug":
            buildType = "--debug"
        else:
            buildType = "--release"
        files = []
        for pattern in ["**/*.dll", "**/*.exe"]:
            files.extend(glob.glob(os.path.join(self.imageDir(), pattern), recursive=True))
        for f in files:
            self.system(["windeployqt" , buildType, "--dir", os.path.join(self.archiveDir(), "bin"),
                         "--qmldir", self.sourceDir(), f])
        return True

    def createPackage(self):
        self.deployQt = False
        self.defines["productname"] = "GammaRay"
        self.defines["website"] = "http://www.kdab.com/gammaray"
        self.defines["company"] = "Klarälvdalens Datakonsult AB"
        self.defines["executable"] = "bin\\gammaray-launcher.exe"
        self.defines["license"] = os.path.join(self.sourceDir(), "LICENSE.GPL.txt")
        self.defines["icon"] = os.path.join(self.sourceDir(), "ui", "resources", "gammaray", "GammaRay.ico")
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("win32libs/icu")
        self.ignoredPackages.append("win32libs/dbus")
        # we are using windeploy
        self.ignoredPackages.extend(CraftPackageObject.get("libs/qt5").children.values())
        return TypePackager.createPackage(self)
