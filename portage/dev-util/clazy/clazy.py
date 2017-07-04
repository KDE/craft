# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
      self.runtimeDependencies['virtual/base'] = 'default'
      self.runtimeDependencies['win32libs/llvm'] = 'default'

        
    def setTargets( self ):
      self.svnTargets['master'] = '[git]kde:clazy'
      self.defaultTarget = 'master'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.supportsClang = False
        if compiler.isMSVC():
            clangLib =  os.path.join(portage.getPackageInstance('win32libs', 'llvm').buildDir(), "lib", "clang.lib")
            self.subinfo.options.configure.defines = f"-DCLANG_LIBRARY_IMPORT='{clangLib}'"

    def configureOptions(self, defines=""):
        options = CMakePackageBase.configureOptions(self, defines)
        # just expect that we don't want to debug our compiler
        options += ' -DCMAKE_BUILD_TYPE=Release'
        return options
