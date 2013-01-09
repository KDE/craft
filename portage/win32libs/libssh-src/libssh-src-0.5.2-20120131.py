# -*- coding: utf-8 -*-
import compiler
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['0.4.4', '0.4.6', '0.4.7']:
            self.targets[ ver ] = "http://www.libssh.org/files/0.4/libssh-" + ver + ".tar.gz"
            self.targetInstSrc[ ver ] = "libssh-" + ver
        for ver in ['0.5.0', '0.5.2']:
            self.targets[ ver ] = "http://www.libssh.org/files/0.5/libssh-" + ver + ".tar.gz"
            self.targetInstSrc[ ver ] = "libssh-" + ver
        self.targetDigests['0.4.4'] = 'bde1d4713a86b6256ce2d14e6de6326e52c4da44'
        self.targetDigests['0.4.6'] = '52e7e68590fbcd835bc4a2eceb51e672641efb69'
        self.targetDigests['0.4.7'] = '5e31736ff906e745e6da508828685d8389e37954'
        self.targetDigests['0.5.0'] = 'ec72a2e23f97d412c465f8ba97d688679550ac18'
        self.patchToApply['0.4.7'] = [("libssh-0.4.7-20110116.diff", 1)]
        self.patchToApply['0.5.0'] = [("libssh-0.5.0-20110601.diff", 1)]
        self.patchToApply['0.5.2'] = [("0001-implement-support-for-putty-s-pageant.patch", 1), 
                                      ("0002-add-a-way-to-test-ssh-connections-on-windows.patch", 1)]

        self.svnTargets['gitHEAD'] = "git://git.libssh.org/projects/libssh.git"
        self.svnTargets['0.4'] = "git://git.libssh.org/projects/libssh.git|v0-4"
        self.svnTargets['0.5'] = "git://git.libssh.org/projects/libssh.git|v0-5"
        self.shortDescription = "a working SSH implementation by the mean of a library"
        self.defaultTarget = '0.5.2'
        self.options.configure.defines = "-DWITH_STATIC_LIB=ON"

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.dependencies['win32libs/openssl'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)


if __name__ == '__main__':
    Package().execute()
