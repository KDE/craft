# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/bangarang/bangarang.git'
        self.defaultTarget = 'gitHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        
if __name__ == '__main__':
    Package().execute()