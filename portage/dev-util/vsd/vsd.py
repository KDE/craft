# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
      self.buildDependencies['virtual/base'] = 'default'

        
    def setTargets( self ):
      self.svnTargets['gitHEAD'] = 'https://github.com/TheOneRing/vsd.git'
      self.defaultTarget = 'gitHEAD'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
