# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
      self.dependencies['libs/qt'] = 'default'
      self.dependencies['kdesupport/hupnp'] = 'default'

        
    def setTargets( self ):
      self.svnTargets['gitHEAD'] = '[git]kde:kio-upnp-ms'
      self.defaultTarget = 'gitHEAD'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

