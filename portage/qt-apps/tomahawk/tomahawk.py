# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['libs/qt5'] = 'default'
        self.hardDependencies['qt-libs/quazip'] = 'default'
        self.hardDependencies['qt-libs/libjreen'] = 'default'
        #self.hardDependencies['qt-libs/qtsparkle'] = 'default
        self.hardDependencies['qt-libs/qtkeychain'] = 'default'
        # self.hardDependencies['qt-libs/qtweetlib'] = 'default'
        self.hardDependencies['kdesupport/phonon'] = 'default'
        self.hardDependencies['kdesupport/phonon-vlc'] = 'default'
        self.hardDependencies['kdesupport/qca'] = 'default'
        self.hardDependencies['kdesupport/libechonest'] = 'default'
        self.hardDependencies['kde/attica'] = 'default'
        self.hardDependencies['kdesupport/liblastfm'] = 'default'
        self.hardDependencies['win32libs/clucene-core'] = 'default'
        self.hardDependencies['win32libs/taglib'] = 'default'
        self.hardDependencies['win32libs/websocketpp'] = 'default'
        
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://github.com/tomahawk-player/tomahawk.git'
        self.defaultTarget = 'gitHEAD'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = " -DWITH_BREAKPAD=OFF -DWITH_CRASHREPORTER=OFF -DBUILD_WITH_QT4=OFF -DWITH_KDE4=OFF -DBUILD_HATCHET=ON"

