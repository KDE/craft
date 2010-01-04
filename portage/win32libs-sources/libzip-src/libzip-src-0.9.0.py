# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.9.0'] = "http://www.nih.at/libzip/libzip-0.9.tar.bz2"
        self.targetInstSrc['0.9.0'] = "libzip-0.9"
        self.patchToApply['0.9.0'] = ( 'libzip-0.9.diff', 1 )
        self.defaultTarget = '0.9.0'
        self.options.package.withCompiler = False

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()