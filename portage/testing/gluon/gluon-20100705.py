# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/gluon/gluon.git'
        self.defaultTarget = 'gitHEAD'
        
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['testing/openal-soft-src'] = 'default'
        self.hardDependencies['testing/libsndfile-src'] = 'default'
        self.hardDependencies['testing/glew-src'] = 'default'
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        
if __name__ == '__main__':
    Package().execute()