# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qt3d"] = "default"
        self.runtimeDependencies["qt-libs/quazip"] = "default"
        self.runtimeDependencies["qt-libs/libjreen"] = "default"
        # self.runtimeDependencies["qt-libs/qtsparkle"] = "default"
        self.runtimeDependencies["qt-libs/qtkeychain"] = "default"
        # self.runtimeDependencies["qt-libs/qtweetlib"] = "default"
        self.runtimeDependencies["binary/vlc"] = "default"
        self.runtimeDependencies["kdesupport/qca"] = "default"
        self.runtimeDependencies["qt-libs/libechonest"] = "default"
        self.runtimeDependencies["frameworks/tier1/attica"] = "default"
        self.runtimeDependencies["qt-libs/liblastfm"] = "default"
        self.runtimeDependencies["win32libs/luceneplusplus"] = "default"
        self.runtimeDependencies["win32libs/taglib"] = "default"
        self.runtimeDependencies["win32libs/gnutls"] = "default"
        self.buildDependencies["win32libs/websocketpp"] = "default"
        self.runtimeDependencies["win32libs/libsparsehash"] = "default"

    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/tomahawk-player/tomahawk.git'
        self.defaultTarget = 'master'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = " -DWITH_CRASHREPORTER=OFF -DBUILD_WITH_QT4=OFF -DWITH_KDE4=OFF -DBUILD_HATCHET=ON"
