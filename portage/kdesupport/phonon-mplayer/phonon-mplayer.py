# -*- coding: utf-8 -*-
import os

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
      self.hardDependencies['testing/mplayer'] = 'default'

    def setTargets( self ):
      self.svnTargets['gitHEAD'] = '[git]kde:phonon-mplayer'
      self.defaultTarget = 'gitHEAD'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = '-DPHONON_BUILDSYSTEM_DIR=\"%s\" ' % os.path.join(emergeRoot(),'share','phonon-buildsystem').replace('\\','/')


