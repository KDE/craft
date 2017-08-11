# -*- coding: utf-8 -*-

import info
from CraftOS.osutils import OsUtils
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/quassel/quassel.git'
        self.svnTargets['0.6'] = 'git://gitorious.org/quassel/quassel.git|0.6|'
        for ver in ['0.7.1', '0.7.2', '0.7.3', '0.8.0', '0.9.0', '0.9.1', '0.9.2', '0.9.3', '0.10.0', '0.11.0',
                    '0.12-rc1', '0.12.0', '0.12.2']:
            self.targets[ver] = 'http://quassel-irc.org/pub/quassel-%s.tar.bz2' % ver
            self.targetInstSrc[ver] = 'quassel-%s' % ver
        self.targetDigests['0.7.1'] = '791086da977033a1bbee3effa317668b3726bd7f'
        self.targetDigests['0.8.0'] = 'b74967fa9f19b5d7c708279075cc0ef3a3dbbe8b'
        self.targetDigests['0.10.0'] = '305d56774b1af2a891775a5637174d9048d875a7'
        self.targetDigests['0.11.0'] = 'd7b31f8e1ee4465ec33dd77f689fec59f4b78a36'
        self.targetDigests['0.12.2'] = '12e9a88597f724498c40a1548b5f788e7c40858c'
        self.patchToApply['0.11.0'] = ('quassel-0.11.0-20141002.diff', 1)

        self.webpage = "http://quassel-irc.org"
        self.defaultTarget = '0.12.2'

    def setDependencies(self):
        self.runtimeDependencies["qt-libs/snorenotify"] = "default"
        self.runtimeDependencies["win32libs/zlib"] = "default"
        self.runtimeDependencies["win32libs/openssl"] = "default"
        # self.runtimeDependencies["kdesupport/qca"] = "default"
        self.runtimeDependencies["dev-util/pkg-config"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebengine"] = "default"
        self.runtimeDependencies["libs/qt5/qtscript"] = "default"
        self.runtimeDependencies["libs/qt5/qttools"] = "default"
        self.description = "a distributed IRC client"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.supportsNinja = OsUtils.isWin()
        self.subinfo.options.configure.args = " -DUSE_QT5=ON -DCMAKE_DISABLE_FIND_PACKAGE_Qt5DBus=ON"

    def install(self):
        if not CMakePackageBase.install(self):
            return False
        if OsUtils.isWin():
            os.makedirs(os.path.join(self.installDir(), "bin"))
            shutil.move(os.path.join(self.installDir(), "quassel.exe"),
                        os.path.join(self.installDir(), "bin", "quassel.exe"))
            shutil.move(os.path.join(self.installDir(), "quasselcore.exe"),
                        os.path.join(self.installDir(), "bin", "quasselcore.exe"))
            shutil.move(os.path.join(self.installDir(), "quasselclient.exe"),
                        os.path.join(self.installDir(), "bin", "quasselclient.exe"))
        return True

    def preArchive(self):
        utils.mergeTree(os.path.join(self.archiveDir(), "bin"), self.archiveDir())
        return True

    def createPackage(self):
        self.blacklist_file = [
            PackagerLists.runtimeBlacklist,
            os.path.join(self.packageDir(), 'blacklist.txt')
        ]
        self.whitelist_file = [
            os.path.join(self.packageDir(), 'whitelist.txt')
        ]
        self.defines["gitDir"] = self.sourceDir()
        self.defines["caption"] = self.binaryArchiveName(fileType=None).capitalize()
        self.defines["productname"] = None
        self.defines["company"] = None

        self.scriptname = os.path.join(self.sourceDir(), "scripts", "build", "NullsoftInstaller.nsi")
        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)
