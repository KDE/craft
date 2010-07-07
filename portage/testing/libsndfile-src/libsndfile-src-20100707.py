# -*- coding: utf-8 -*-
import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.0.21'] = 'http://www.mega-nerd.com/libsndfile/files/libsndfile-1.0.21.tar.gz'
        self.targetInstSrc['1.0.21'] = 'libsndfile-1.0.21'
        self.options.package.withCompiler = False
        self.options.package.packageName = "libsndfile"
        self.defaultTarget = '1.0.21'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        self.subinfo.options.configure.defines = " -DBUILD_SHARED_LIB=ON"
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
