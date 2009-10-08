# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://git.libssh.org/projects/libssh/libssh.git"
        self.defaultTarget = 'gitHEAD'
        self.options.package.withCompiler = False
        self.subinfo.options.configure.defines = "-DWITH_STATIC_LIB=ON"

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        
if __name__ == '__main__':
    Package().execute()
