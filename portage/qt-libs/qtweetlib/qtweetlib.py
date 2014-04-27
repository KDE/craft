# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
      self.hardDependencies[ 'libs/qt' ] = 'default'
      self.hardDependencies[ 'kdesupport/qjson' ] = 'default'

    def setTargets( self ):
      self.svnTargets[ 'gitHEAD' ] = 'https://github.com/minimoog/QTweetLib.git'
      self.targets['0.5'] = 'http://cloud.github.com/downloads/minimoog/QTweetLib/QTweetLib-0.5.tar.gz'
      self.targetDigests['0.5'] = 'cab78a68294d0b79e9108a180e2cd9da225581b0'
      self.targetInstSrc['0.5'] = 'QTweetLib-0.5'
      self.defaultTarget = '0.5'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
