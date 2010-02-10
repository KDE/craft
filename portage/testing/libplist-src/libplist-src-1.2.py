# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://github.com/JonathanBeck/libplist.git'
        self.defaultTarget = 'gitHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'
        self.hardDependencies['virtual/base'] = 'default'
    
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)


if __name__ == '__main__':
    Package().execute()
