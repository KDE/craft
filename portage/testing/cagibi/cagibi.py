# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
      self.hardDependencies['libs/qt'] = 'default'
      self.hardDependencies['kdesupport/hupnp'] = 'default'

        
    def setTargets( self ):
      self.svnTargets['gitHEAD'] = '[git]kde:cagibi'
      self.svnTargets['0.1'] = '[git]kde:cagibi|0.1|'
      self.defaultTarget = '0.1'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

