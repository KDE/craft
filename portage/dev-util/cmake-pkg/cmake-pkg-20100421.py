# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://cmake.org/cmake.git"
        self.svnTargets['release'] = "git://cmake.org/cmake.git|release|"
        self.svnTargets['v2.8.2'] = "git://cmake.org/cmake.git|release|v2.8.2"
        for ver in ['2.8.0', '2.8.1', '2.8.2', '2.8.3', '2.8.8','2.8.10.2']:
            self.targets[ ver ] = "http://www.cmake.org/files/v2.8/cmake-" + ver + ".tar.gz"
            self.targetInstSrc[ ver ] = "cmake-" + ver
        self.patchToApply['2.8.0'] = ("cmake-2.8.0-20100512.diff", 1)
        self.patchToApply['2.8.1'] = ("cmake-2.8.1-20100511.diff", 1)
        self.patchToApply['2.8.3'] = ("cmake-2.8.3-20101222.diff", 1)
        self.patchToApply['2.8.8'] = ("cmake-2.8.3-20101222.diff", 1)
        self.patchToApply['2.8.10.2'] = ("cmake-2.8.10.diff", 1)
        self.targetDigests['2.8.10.2'] = '2d868ccc3f9f2aa7c2844bd0a4609d5313edaaec'
        self.defaultTarget = '2.8.10.2'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.merge.destinationPath = "dev-utils"

if __name__ == '__main__':
    Package().execute()
