# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
      self.hardDependencies['testing/vlc'] = 'default'
      if COMPILER == "msvc2008":
        self.hardDependencies['kdesupport/kdewin'] = 'default'
        
    def setTargets( self ):
      self.svnTargets['gitHEAD'] = 'git://gitorious.org/phonon/phonon-vlc.git'
      self.defaultTarget = 'gitHEAD'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)       
        if COMPILER == "msvc2008":
            self.subinfo.options.configure.defines = ' -DCMAKE_INCUDE_PATH=%s/include/msvc' % self.mergeDestinationDir()

if __name__ == '__main__':
    Package().execute()
