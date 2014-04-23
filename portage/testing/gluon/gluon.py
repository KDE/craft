# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:gluon.git'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['testing/openal-soft-src'] = 'default'
        self.dependencies['win32libs/libsndfile'] = 'default'
        self.dependencies['win32libs/glee'] = 'default'
        self.dependencies['testing/alure-src'] = 'default'
        self.dependencies['win32libs/glew'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
