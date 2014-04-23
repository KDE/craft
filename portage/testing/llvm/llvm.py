# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "http://llvm.org/svn/llvm-project/llvm/trunk"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        # this program needs python 2.7
        self.subinfo.options.configure.defines = "-DPYTHON_EXECUTABLE=C:/python27_x86/python.exe"

if __name__ == '__main__':
    Package().execute()
