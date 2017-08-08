# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.9.16']:
            self.targets[ver] = 'https://github.com/LMDB/lmdb/archive/LMDB_' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'lmdb-LMDB_' + ver + '/libraries/liblmdb'
        self.patchToApply['0.9.16'] = [('lmdb-LMDB_0.9.16-20151004.diff', 3)]
        self.targetDigests['0.9.16'] = '367182e1d9dbc314db76459a71be719209f131b4'

        self.description = 'in memory database from the openldap project'
        self.defaultTarget = '0.9.16'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DBUILD_TESTS=OFF -DBUILD_TOOLS=OFF"
