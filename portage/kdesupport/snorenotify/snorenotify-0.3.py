# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
      self.shortDescription = "An application to show kde notifications with Snarl/Growl"
      self.hardDependencies['libs/qt'] = 'default'
      self.hardDependencies['win32libs/boost-system'] = 'default'
      self.hardDependencies['win32libs/boost-thread'] = 'default'
      self.hardDependencies['kde/kdelibs'] = 'default'
      self.buildDependencies['win32libs/cryptopp'] = 'default'


    def setTargets( self ):
      self.svnTargets['gitHEAD'] = 'git@github.com:TheOneRing/Snorenotify.git'
      for ver in ['0.2','0.3','0.4-beta1','0.4-beta2']:
          self.targets[ver] = 'https://github.com/TheOneRing/Snorenotify/archive/v%s.tar.gz' % ver
          self.targetInstSrc[ver] = 'Snorenotify-%s' % ver
      self.targetDigests['0.4-beta1'] = '76996e2ebd23fa7b99b68e743c880b3fa0d724af'
      self.defaultTarget = '0.4-beta2'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = ' -DWITH_FREEDESKTOP_FRONTEND=ON -DWITH_SNORE_DEAMON=ON '

if __name__ == '__main__':
    Package().execute()
