# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
      self.hardDependencies[ 'libs/qt' ] = 'default'
      self.hardDependencies[ 'kdesupport/qjson' ] = 'default'

    def setTargets( self ):
      self.svnTargets[ 'gitHEAD' ] = '[git]kde:libechonest'
      for ver in ['1.2.1','2.0.1']:
        self.targets[ver] = 'http://pwsp.cleinias.com/libechonest-%s.tar.bz2' % ver
        self.targetInstSrc[ver] = 'libechonest-%s' % ver
      self.targetDigests['1.2.1'] = '5ad5897c91c365b32840e75e806c9725c89b4522'
      self.targetDigests['2.0.1'] = '5dd98ffb370e0e199e37ece4a1775a05594f3dcb'
      self.defaultTarget = '2.0.1'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
#        self.subinfo.options.configure.defines = "-DECHONEST_BUILD_TESTS=OFF"

if __name__ == '__main__':
    Package().execute()
