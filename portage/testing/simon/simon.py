# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
      self.svnTargets['gitHEAD'] = '[git]kde:simon'
      self.defaultTarget = 'gitHEAD'
      
    def setDependencies( self ):
      self.buildDependencies['dev-util/winflexbison'] = 'default'
      self.dependencies['win32libs/libfl'] = 'default'
      self.buildDependencies['dev-util/gettext-tools'] = 'default'
      self.dependencies['libs/qt'] = 'default'
      self.dependencies['win32libs/gettext'] = 'default'
      self.dependencies['kdesupport/qwt6'] = 'default'
      self.dependencies['win32libs/libsamplerate'] = 'default'
      self.dependencies['kde/kdepimlibs'] = 'default'

         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

