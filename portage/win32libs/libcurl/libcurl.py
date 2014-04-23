# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://github.com/bagder/curl.git"
        for ver in [ '7.20.0', '7.28.1', '7.32.0' ]:
            self.targets[ver] = 'http://curl.haxx.se/download/curl-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'curl-' + ver
        self.patchToApply['7.20.0'] = ("7.20.0.diff", 1)
        self.patchToApply['7.28.1'] = [("curl-7.28.1-20130202.diff", 1),
                                       ("curl-7.28.1-installlocation.diff", 1)]
        self.patchToApply['7.32.0'] = [("curl-7.32.0-20130901.diff", 1),
                                       ("curl-7.28.1-installlocation.diff", 1)]
        self.targetDigests['7.28.1'] = 'b5aff1afc4e40fcb78db7a5e27214e0035756f3d'
        self.targetDigests['7.32.0'] = 'f6989fca0dac0c35628523436fc17869972d4251'

        self.shortDescription = "a free and easy-to-use client-side URL transfer library"
        self.defaultTarget = '7.32.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.dependencies['win32libs/openssl'] = 'default'


class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = " -DBUILD_CURL_TESTS=OFF"
        self.subinfo.options.configure.testDefine = "-DBUILD_CURL_TESTS=ON"
        self.subinfo.options.configure.toolsDefine = "-DBUILD_CURL_EXE=ON"
        self.subinfo.options.configure.staticDefine = "-DCURL_STATICLIB=ON"

if __name__ == '__main__':
    Package().execute()

