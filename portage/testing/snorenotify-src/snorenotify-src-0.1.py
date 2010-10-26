# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
      self.hardDependencies['libs/qt'] = 'default'

        
    def setTargets( self ):
      self.svnTargets['gitHEAD'] = 'git://gitorious.org/snorenotify/snorenotify.git'
      self.defaultTarget = 'gitHEAD'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)       
        self.subinfo.options.configure.defines = ' -DWITH_FREEDESKTOP_FRONTEND=ON'

if __name__ == '__main__':
    Package().execute()
