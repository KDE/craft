# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
      self.hardDependencies[ 'libs/qt' ] = 'default'
      self.hardDependencies[ 'kdesupport/qjson' ] = 'default'
        
    def setTargets( self ):
      self.svnTargets[ 'gitHEAD' ] = 'git://git.kde.org/libechonest'
      self.defaultTarget = 'gitHEAD'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
#        self.subinfo.options.configure.defines = "-DECHONEST_BUILD_TESTS=OFF"

if __name__ == '__main__':
    Package().execute()
