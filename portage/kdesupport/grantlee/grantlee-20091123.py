# -*- coding: utf-8 -*-
import info
import platform

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://gitorious.org/grantlee/grantlee.git"
        self.svnTargets['0.1'] = "git://gitorious.org/grantlee/grantlee.git|0.1"
        self.defaultTarget = '0.1'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        if not platform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines = '-DBUILD_TESTS=OFF'
        CMakePackageBase.__init__(self)
        
if __name__ == '__main__':
    Package().execute()
