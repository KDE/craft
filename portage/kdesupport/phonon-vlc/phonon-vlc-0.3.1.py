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
      self.targets['0.3.1'] = "http://download.kde.org/download.php?url=stable/phonon-backend-vlc/0.3.1/src/phonon-backend-vlc-0.3.1.tar.bz2"
      self.targetInstSrc['0.3.1'] = "phonon-backend-vlc-0.3.1"
      self.targetDigests['0.3.1'] = 'b94dddc6f37924c101a8bab7b7a184b7d6b42d96'
      self.svnTargets['gitHEAD'] = 'git://gitorious.org/phonon/phonon-vlc.git'
      self.defaultTarget = '0.3.1'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)       
        if COMPILER == "msvc2008":
            self.subinfo.options.configure.defines = ' -DCMAKE_INCUDE_PATH=%s/include/msvc' % self.mergeDestinationDir()

if __name__ == '__main__':
    Package().execute()
