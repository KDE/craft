# -*- coding: utf-8 -*-
import info
import portage

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "http://llvm.org/svn/llvm-project/cfe/trunk"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'
        self.dependencies['testing/llvm'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.llvm = portage.getPackageInstance("testing", "llvm")
        self.subinfo.options.configure.defines = "-DCLANG_PATH_TO_LLVM_BUILD=" + self.llvm.imageDir()

if __name__ == '__main__':
    Package().execute()
