# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/libjpeg-turbo/libjpeg-turbo.git"

        for ver in ["1.5.1"]:
            self.targets[ver] = "https://github.com/libjpeg-turbo/libjpeg-turbo/archive/%s.tar.gz" % ver
            self.archiveNames[ver] = "libjpeg-turbo-%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'libjpeg-turbo-%s' % ver

        self.targetDigests['1.5.1'] = (
            ['c15a9607892113946379ccea3ca8b85018301b200754f209453ab21674268e77'], CraftHash.HashAlgorithm.SHA256)

        self.description = "libjpeg-turbo is a JPEG image codec that uses SIMD instructions (MMX, SSE2, NEON, AltiVec) to accelerate baseline JPEG compression and decompression on x86, x86-64, ARM, and PowerPC systems"
        self.webpage = "http://libjpeg-turbo.virtualgl.org/"
        self.defaultTarget = '1.5.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/nasm"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
