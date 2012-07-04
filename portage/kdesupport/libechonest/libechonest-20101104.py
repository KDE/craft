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
      self.targets['1.2.1'] = 'http://pwsp.cleinias.com/libechonest-1.2.1.tar.bz2'
      self.targetInstSrc['1.2.1'] = 'libechonest-1.2.1'
      self.targetDigests['1.2.1'] = '5ad5897c91c365b32840e75e806c9725c89b4522'
      self.defaultTarget = '1.2.1'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
#        self.subinfo.options.configure.defines = "-DECHONEST_BUILD_TESTS=OFF"

if __name__ == '__main__':
    Package().execute()
