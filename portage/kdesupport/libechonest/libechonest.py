# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
      self.dependencies[ 'libs/qtbase' ] = 'default'
      self.buildDependencies[ 'win32libs/boost-headers' ] = 'default'

    def setTargets( self ):
      self.svnTargets[ 'gitHEAD' ] = '[git]kde:libechonest'
      for ver in ['1.2.1','2.0.1','2.0.2','2.0.3']:
        self.targets[ver] = 'http://files.lfranchi.com/libechonest-%s.tar.bz2' % ver
        self.targetInstSrc[ver] = 'libechonest-%s' % ver
      self.targetDigests['1.2.1'] = '5ad5897c91c365b32840e75e806c9725c89b4522'
      self.targetDigests['2.0.1'] = '5dd98ffb370e0e199e37ece4a1775a05594f3dcb'
      self.targetDigests['2.0.2'] = '346eba6037ff544f84505941832604668c1e5b2b'
      self.targetDigests['2.0.3'] = '10ada8aced6dce3c0d206afcfbd4b05313bd4d04'
      self.patchToApply['2.0.3'] = ('libechonest-2.0.3-20130419.diff',1)
      self.defaultTarget = 'gitHEAD'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_WITH_QT4=OFF "

