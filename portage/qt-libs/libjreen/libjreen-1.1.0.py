# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
      self.hardDependencies[ 'libs/qt' ] = 'default'

    def setTargets( self ):
      self.svnTargets[ 'gitHEAD' ] = 'git://github.com/euroelessar/jreen.git'
      self.targets['1.1.0'] = 'http://qutim.org/downloads/libjreen-1.1.0.tar.bz2'
      self.targetDigests['1.1.0'] = '2636a25e62d8e2acd13626add77db288a48ca729'
      self.targetInstSrc['1.1.0'] = 'libjreen-1.1.0'
      self.defaultTarget = '1.1.0'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
