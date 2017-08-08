import info

from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = 'Yet Another JSON Library'

        self.svnTargets['master'] = 'https://github.com/lloyd/yajl'

        ver = '1.0.12'

        self.targets[ver] = 'http://github.com/lloyd/yajl/tarball/%s' % ver
        self.archiveNames[ver] = 'lloyd-yajl-%s.tar.gz' % ver
        self.targetDigests[ver] = 'f0177e3a946d6ae9a0a963695b2c143a03219bf2'
        self.patchToApply[ver] = ('lloyd-yajl-17b1790-20110725.diff', 1)
        self.targetInstSrc[ver] = 'lloyd-yajl-17b1790'

        self.defaultTarget = ver

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
