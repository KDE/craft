# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
      self.hardDependencies['testing/vlc'] = 'default'
        
    def setTargets( self ):
      self.svnTargets['gitHEAD'] = 'git://gitorious.org/phonon/phonon-vlc.git'
      self.defaultTarget = 'gitHEAD'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)       

if __name__ == '__main__':
    Package().execute()
