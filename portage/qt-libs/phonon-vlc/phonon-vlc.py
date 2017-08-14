# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["qt-libs/phonon"] = "default"
        self.runtimeDependencies["binary/vlc"] = "default"
        if craftCompiler.isMSVC() or craftCompiler.isIntel():
            self.runtimeDependencies["kdesupport/kdewin"] = "default"

    def setTargets(self):
        for ver in ['0.9.0']:
            self.targets[
                ver] = "http://download.kde.org/stable/phonon/phonon-backend-vlc/%s/phonon-backend-vlc-%s.tar.xz" % (
            ver, ver)
            self.targetInstSrc[ver] = "phonon-vlc-%s" % ver

        self.targetDigests['0.9.0'] = (
            ['c0ced7ca571acc22211eecf5158241714fa9ccdb82d4fe0a970ad702860ccdbe'], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets['master'] = '[git]kde:phonon-vlc'

        self.description = "the vlc based phonon multimedia backend"
        self.defaultTarget = '0.9.0'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = ' -DCMAKE_CXX_FLAGS=-DWIN32  -DPHONON_BUILD_PHONON4QT5=ON -DPHONON_BUILDSYSTEM_DIR=\"%s\" ' % (
        os.path.join(CraftStandardDirs.craftRoot(), 'share', 'phonon', 'buildsystem').replace('\\', '/'))
