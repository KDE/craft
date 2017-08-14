# -*- coding: utf-8 -*-

import info
from Package.Qt5CorePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/KDAB/KDSoap.git"
        for ver in ["1.6.0"]:
            self.targets[ver] = f"https://github.com/KDAB/KDSoap/releases/download/kdsoap-{ver}/kdsoap-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"kdsoap-{ver}"
        self.targetDigests['1.6.0'] = (
            ['d6b6b01348d2e1453f7e12724d1848ee41c86a1b19168ca67ac98fedb0408668'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.6.0"
        self.description = "A Qt-based client-side and server-side SOAP component"
        self.webpage = "http://www.kdab.com/products/kd-soap"

    def setDependencies(self):
        self.buildDependencies["dev-util/python2"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)

    def configure(self):
        self.enterBuildDir()
        buildType = "release"
        if self.buildType() == "Debug":
            buildType = "debug"
        ext = ".bat" if OsUtils.isWin() else ".sh"
        prefix = CraftStandardDirs.craftRoot().replace("\\", "/")
        if not os.path.isfile(os.path.join(self.sourceDir(), f"configure{ext}")):
            return self.system(f"python2 {self.sourceDir()}/autogen.py -prefix {prefix} -shared -{buildType}")
        else:
            with open(os.path.join(self.buildDir(), ".license.accepted"), "wt+") as touch:  # build lgpl
                touch.write("can't touch this")
            return self.system(f"{self.sourceDir()}/configure{ext} -prefix {prefix} -shared -{buildType}")

    def install(self):
        if not Qt5CorePackageBase.install(self):
            return False
        for f in os.listdir(os.path.join(self.installDir(), "lib")):
            if f.endswith(".dll"):
                utils.copyFile(os.path.join(self.installDir(), "lib", f),
                               os.path.join(self.installDir(), "bin", f))
        return True
