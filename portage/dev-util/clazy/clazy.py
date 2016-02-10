# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
      self.buildDependencies['virtual/base'] = 'default'
      self.dependencies['win32libs/llvm'] = 'default'

        
    def setTargets( self ):
      self.svnTargets['gitHEAD'] = '[git]kde:clazy'
      self.defaultTarget = 'gitHEAD'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.supportsClang = False
        self.subinfo.options.configure.defines = "-DCLAZY_ON_WINDOWS_HACK=ON"

    def configureOptions(self, defines=""):
        options = CMakePackageBase.configureOptions(self, defines)
        # just expect that we don't want to debug our compiler
        options += ' -DCMAKE_BUILD_TYPE=Release'
        return options
