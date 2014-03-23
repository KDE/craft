# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
      self.shortDescription = "An application to show kde notifications with Snarl/Growl"
      self.hardDependencies['libs/qtbase'] = 'default'
      self.hardDependencies['win32libs/boost-system'] = 'default'
      self.hardDependencies['win32libs/boost-thread'] = 'default'
      self.buildDependencies['win32libs/cryptopp'] = 'default'


    def setTargets( self ):
      self.svnTargets['gitHEAD'] = 'git@github.com:TheOneRing/Snorenotify.git'
      self.svnTargets['0.5'] = 'git@github.com:TheOneRing/Snorenotify.git|0.5'
      for ver in ['0.2','0.3','0.4-beta1','0.4-beta2']:
          self.targets[ver] = 'https://github.com/TheOneRing/Snorenotify/archive/v%s.tar.gz' % ver
          self.archiveNames[ver] = "snorenotify-%s.tar.gz" % ver
          self.targetInstSrc[ver] = 'Snorenotify-%s' % ver
      self.targetDigests['0.4-beta1'] = '76996e2ebd23fa7b99b68e743c880b3fa0d724af'
      self.defaultTarget = '0.5'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = ' -DWITH_KDE=OFF -DWITH_QT4=OFF -DWITH_FREEDESKTOP_FRONTEND=ON -DWITH_SNORE_DEAMON=ON '

if __name__ == '__main__':
    Package().execute()
