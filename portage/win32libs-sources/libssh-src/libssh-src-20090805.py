# -*- coding: utf-8 -*-
import compiler
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.4.4'] = "http://www.libssh.org/files/libssh-0.4.4.tar.gz"
        self.targetDigests['0.4.4'] = 'bde1d4713a86b6256ce2d14e6de6326e52c4da44'
        self.targetInstSrc['0.4.4'] = "libssh-0.4.4"
        self.svnTargets['gitHEAD'] = "git://git.libssh.org/projects/libssh/libssh.git"
        self.svnTargets['0.4'] = "git://git.libssh.org/projects/libssh/libssh.git|v0-4"

        self.defaultTarget = '0.4.4'
        self.options.configure.defines = "-DWITH_STATIC_LIB=ON"

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/zlib'] = 'default'
        self.dependencies['win32libs-bin/openssl'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        if self.buildTarget == 'gitHEAD':
            self.subinfo.options.package.withCompiler = True

        
if __name__ == '__main__':
    Package().execute()
