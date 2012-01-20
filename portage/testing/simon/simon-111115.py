# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
      self.svnTargets['gitHEAD'] = 'git:simon'
      self.defaultTarget = 'gitHEAD'
      
    def setDependencies( self ):
      self.buildDependencies['gnuwin32/flex'] = 'default'
      self.buildDependencies['gnuwin32/bison'] = 'default'
      self.buildDependencies['dev-util/gettext-tools'] = 'default'
      self.dependencies['libs/qt'] = 'default'
      self.dependencies['win32libs-bin/gettext'] = 'default'
      self.dependencies['kdesupport/qwt6'] = 'default'
      self.dependencies['win32libs-bin/libsamplerate'] = 'default'
      self.dependencies['kde/kdepimlibs'] = 'default'

         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
