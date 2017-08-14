# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['3.8.0'] = 'https://github.com/sqlitebrowser/sqlitebrowser/archive/v3.8.0.tar.gz'
        self.archiveNames['3.8.0'] = "sqlitebrowser-3.8.0.tar.gz"
        self.targetInstSrc['3.8.0'] = 'sqlitebrowser-3.8.0'
        self.targetDigests['3.8.0'] = (
            ['f638a751bccde4bf0305a75685e2a72d26fc3e3a69d7e15fd84573f88c1a4d92'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = '3.8.0'
        self.description = "DB Browser for SQLite"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DUSE_QT5=ON"
