# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
      self.svnTargets['gitHEAD'] = 'git://speech2text.git.sourceforge.net/gitroot/speech2text/speech2text||windows'
      self.defaultTarget = 'gitHEAD'
      
    def setDependencies( self ):
      self.buildDependencies['gnuwin32/flex'] = 'default'
      self.buildDependencies['gnuwin32/bison'] = 'default'
      self.buildDependencies['dev-util/gettext-tools'] = 'default'
      self.hardDependencies['libs/qt'] = 'default'
      self.hardDependencies['win32libs-bin/gettext'] = 'default'
      self.hardDependencies['kdesupport/qwt6'] = 'default'
      self.hardDependencies['win32libs-bin/libsamplerate'] = 'default'
      self.hardDependencies['kde/kdepimlibs'] = 'default'

         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
