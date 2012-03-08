# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
      self.shortDescription = "An application to show kde notifications with Snarl/Growl"
      self.hardDependencies['libs/qt'] = 'default'
      self.hardDependencies['win32libs-bin/boost-system'] = 'default'
      self.hardDependencies['win32libs-bin/boost-thread'] = 'default'
      self.hardDependencies['kde/kdelibs'] = 'default'
      self.buildDependencies['win32libs-bin/cryptopp'] = 'default'


    def setTargets( self ):
      self.svnTargets['gitHEAD'] = 'git://gitorious.org/snorenotify/snorenotify.git'
      for ver in ['0.2','0.3']:
          self.targets[ver] = 'http://winkde.org/~pvonreth/downloads/snore/snore-%s.tar.xz' % ver
      self.targetDigests['0.2'] = '3fcc5dfb69408fef1efb670d6042030daad75580'
      self.targetDigests['0.3'] = '853aa0f531003bce7570c880455edee048c84294'
      self.defaultTarget = 'gitHEAD'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = ' -DWITH_FREEDESKTOP_FRONTEND=ON'

if __name__ == '__main__':
    Package().execute()
