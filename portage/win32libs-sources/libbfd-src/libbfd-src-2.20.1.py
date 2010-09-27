# -*- coding: utf-8 -*-
import info
import os

from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.MultiPackager import *
from Package.PackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.20.1'] = "http://ftp.gnu.org/gnu/binutils/binutils-2.20.1.tar.gz"
        self.targetInstSrc['2.20.1'] = 'binutils-2.20.1/bfd'
        self.targetDigests['2.20.1'] = 'd4428deccc9d1d170929a820d04f5d90a1b524ac'
        self.defaultTarget = '2.20.1'
        

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/msys'] = 'default'
        
class Package(PackageBase, MultiSource, AutoToolsBuildSystem, MultiPackager):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)        
        MultiPackager.__init__(self)

if __name__ == '__main__':
    Package().execute()
