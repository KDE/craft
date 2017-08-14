# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "https://github.com/bagder/curl.git"
        for ver in ['7.20.0', '7.28.1', '7.32.0', '7.46.0', '7.54.0']:
            self.targets[ver] = 'https://curl.haxx.se/download/curl-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'curl-' + ver
        self.patchToApply['7.20.0'] = ("7.20.0.diff", 1)
        self.patchToApply['7.28.1'] = [("curl-7.28.1-20130202.diff", 1),
                                       ("curl-7.28.1-installlocation.diff", 1)]
        self.patchToApply['7.32.0'] = [("curl-7.32.0-20130901.diff", 1),
                                       ("curl-7.28.1-installlocation.diff", 1)]
        self.patchToApply['7.46.0'] = [("curl-7.46.0-20151208.diff", 1)]
        self.targetDigests['7.28.1'] = 'b5aff1afc4e40fcb78db7a5e27214e0035756f3d'
        self.targetDigests['7.32.0'] = 'f6989fca0dac0c35628523436fc17869972d4251'
        self.targetDigests['7.46.0'] = '96fbe5abe8ecfb923e4ab0a579b3d6be43ef0e96'
        self.targetDigests['7.54.0'] = (
            ['f50ebaf43c507fa7cc32be4b8108fa8bbd0f5022e90794388f3c7694a302ff06'], CraftHash.HashAlgorithm.SHA256)

        self.description = "a free and easy-to-use client-side URL transfer library"
        self.defaultTarget = '7.54.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/zlib"] = "default"
        self.runtimeDependencies["win32libs/openssl"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = " -DBUILD_CURL_TESTS=OFF -DBUILD_CURL_EXE=OFF"
        self.subinfo.options.configure.testDefine = "-DBUILD_CURL_TESTS=ON"
        self.subinfo.options.configure.toolsDefine = "-DBUILD_CURL_EXE=ON"
        self.subinfo.options.configure.staticArgs = "-DCURL_STATICLIB=ON"
