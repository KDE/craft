# -*- coding: utf-8 -*-
import info
import os
import shutil
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.3.2'] = 'http://www.fftw.org/fftw-3.2.2.tar.gz'
        self.targetDigests['3.3.2'] = 'd43b799eedfb9408f62f9f056f5e8a645618467b'
        self.targetInstSrc['3.3.2'] = "fftw-3.2.2"

        self.defaultTarget = '3.3.2'

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'
        self.hardDependencies['dev-util/msys'] = 'default'

from Package.AutoToolsPackageBase import *

class Package( AutoToolsPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.package.withCompiler = False
        
if __name__ == '__main__':
     Package().execute()
