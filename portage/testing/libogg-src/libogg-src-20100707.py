# -*- coding: utf-8 -*-
import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.2.0'] = 'http://downloads.xiph.org/releases/ogg/libogg-1.2.0.tar.gz'
        self.targetInstSrc['1.2.0'] = 'libogg-1.2.0'
        self.patchToApply['1.2.0'] = ('libogg-1.2.0-20100707.diff', 1)
        self.targetDigests['1.2.0'] = '135fb812282e08833295c91e005bd0258fff9098'
        self.options.package.withCompiler = False
        self.options.package.packageName = "libogg"
        self.defaultTarget = '1.2.0'

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
