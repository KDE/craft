# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
      self.shortDescription = "An application to show kde notifications with Snarl/Growl"
      self.hardDependencies['libs/qt'] = 'default'
      self.hardDependencies['win32libs-sources/boost'] = 'default'
      self.buildDependencies['testing/cryptopp-src'] = 'default'


    def setTargets( self ):
      self.svnTargets['gitHEAD'] = 'git://gitorious.org/snorenotify/snorenotify.git'
      self.targets['0.1'] = 'http://winkde.org/~pvonreth/downloads/snorenotify-0.1.tar.xz'
      self.targetInstSrc['0.1'] = 'snorenotify-0.1'
      self.targetDigests['0.1'] = '39dea268b29c852a8eb740f440c4dcc51670d6f4'
      self.defaultTarget = '0.1'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = ' -DWITH_FREEDESKTOP_FRONTEND=ON'

if __name__ == '__main__':
    Package().execute()
