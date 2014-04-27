# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
      self.hardDependencies[ 'libs/qt' ] = 'default'
      self.hardDependencies[ 'win32libs/libgsasl' ] = 'default'
      self.hardDependencies[ 'win32libs/gettext' ] = 'default'

    def setTargets( self ):
      self.svnTargets[ 'gitHEAD' ] = 'git://github.com/euroelessar/jreen.git'
      self.targets['1.1.0'] = 'http://qutim.org/downloads/libjreen-1.1.0.tar.bz2'
      self.targetInstSrc['1.1.0'] = 'libjreen-1.1.0'
      self.targetDigests['1.1.0'] = '2636a25e62d8e2acd13626add77db288a48ca729'
      self.targets['1.1.1'] = 'http://qutim.org/dwnl/44/libjreen-1.1.1.tar.bz2'
      self.targetInstSrc['1.1.1'] = 'libjreen-1.1.1'
      self.targetDigests['1.1.1'] = 'a4b1a0b31823cc521733a54e964e599e4e150aa4'
      self.defaultTarget = 'gitHEAD'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

