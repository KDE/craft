# -*- coding: utf-8 -*-
import info
import os


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.20.1'] = "http://ftp.gnu.org/gnu/binutils/binutils-2.20.1.tar.gz"
        self.targetInstSrc['2.20.1'] = 'binutils-2.20.1/bfd'
        self.targetDigests['2.20.1'] = 'd4428deccc9d1d170929a820d04f5d90a1b524ac'
        self.defaultTarget = '2.20.1'
        

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['dev-util/msys'] = 'default'

        
        
from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
