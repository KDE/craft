# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/KDAB/Charm.git'
        self.defaultTarget = 'master'
        self.description = "The Cross-Platform Time Tracker"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtwinextras"] = "default"
        self.runtimeDependencies["qt-libs/qtkeychain"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DCHARM_SIGN_INSTALLER=OFF"

    def createPackage(self):
        if craftSettings.getboolean("QtSDK", "Enabled", False):
            # windeployqt tries to deploy every lib starting with qt5....
            # therefore we need to make sure it can find qt5keychain
            keychain = CraftPackageObject.get("qt-libs/qtkeychain").instance
            utils.copyDir(keychain.imageDir(),
                          os.path.join(craftSettings.get("QtSDK", "Path"), craftSettings.get("QtSDK", "Version"),
                                       craftSettings.get("QtSDK", "Compiler")))

        old = self.subinfo.options.make.makeOptions
        self.subinfo.options.make.makeOptions = "package"
        out = CMakePackageBase.make(self)
        self.subinfo.options.make.makeOptions = old
        if not out:
            return False

        reName = re.compile(r"^Charm-\d+.\d+.*\.exe$")
        for f in os.listdir(self.buildDir()):
            match = reName.match(f)
            if match:
                return utils.copyFile(os.path.join(self.buildDir(), f), os.path.join(self.packageDestinationDir(), f))
