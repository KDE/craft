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
      self.targets['0.2'] = 'http://winkde.org/~pvonreth/downloads/snore/snore-0.2.tar.xz'
      self.targetDigests['0.2'] = '3fcc5dfb69408fef1efb670d6042030daad75580'
      self.defaultTarget = 'gitHEAD'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = ' -DWITH_FREEDESKTOP_FRONTEND=ON'

if __name__ == '__main__':
    Package().execute()
