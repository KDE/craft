# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/quassel/quassel.git'
        self.svnTargets['0.6'] = 'git://gitorious.org/quassel/quassel.git|0.6|'
        self.targets['0.7.1'] = 'http://quassel-irc.org/pub/quassel-0.7.1.tar.bz2'
        self.targetDigests['0.7.1'] = '791086da977033a1bbee3effa317668b3726bd7f'
        self.targetInstSrc['0.7.1'] = 'quassel-0.7.1'
        self.defaultTarget = 'gitHEAD'
    
    def setDependencies( self ):
        self.dependencies['virtual/kdebase-runtime'] = 'default'
     

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = ""
        self.subinfo.options.configure.defines += " -DWITH_KDE=ON"
      


if __name__ == '__main__':
    Package().execute()
