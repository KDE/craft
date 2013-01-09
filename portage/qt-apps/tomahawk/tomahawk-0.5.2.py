# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['qt-libs/quazip'] = 'default'
        self.hardDependencies['qt-libs/libjreen'] = 'default'
        self.hardDependencies['qt-libs/qtsparkle'] = 'default'
        self.hardDependencies['qt-libs/qtweetlib'] = 'default'
        self.hardDependencies['kdesupport/phonon'] = 'default'
        self.hardDependencies['kdesupport/phonon-vlc'] = 'default'
        self.hardDependencies['kdesupport/libechonest'] = 'default'
        self.hardDependencies['kdesupport/attica'] = 'default'
        self.hardDependencies['kdesupport/liblastfm'] = 'default'
        self.hardDependencies['win32libs/taglib'] = 'default'
        
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://github.com/tomahawk-player/tomahawk.git'
        self.defaultTarget = 'gitHEAD'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = " -DWITH_BREAKPAD=OFF -DWITH_CRASHREPORTER=OFF "

if __name__ == '__main__':
    Package().execute()
