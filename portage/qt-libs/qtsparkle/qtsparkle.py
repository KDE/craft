# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo( info.infoclass ):
    def setDependencies( self ):
      self.dependencies[ 'libs/qt' ] = 'default'

    def setTargets( self ):
      self.svnTargets[ 'gitHEAD' ] = 'git://github.com/davidsansome/qtsparkle.git'
      self.defaultTarget = 'gitHEAD'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

