# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['frameworks/extra-cmake-modules'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qttools'] = 'default'
        self.dependencies['libs/qtwebsockets'] = 'default'
        self.dependencies['libs/qtmultimedia'] = 'default'
        self.dependencies['win32libs/snoregrowl'] = 'default'



    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:snorenotify'
        for ver in ['0.6.0', '0.7.0']:
            self.targets[ ver ] = "http://download.kde.org/stable/snorenotify/%s/src/snorenotify-%s.tar.xz" % ( ver ,ver )
            self.targetInstSrc[ ver ] = "snorenotify-%s" % ver
            self.targetDigestUrls[ ver ] = ("http://download.kde.org/stable/snorenotify/%s/src/snorenotify-%s.tar.xz.sha256" % (ver, ver), CraftHash.HashAlgorithm.SHA256)

        self.shortDescription = "Snorenotify is a multi platform Qt notification framework. Using a plugin system it is possible to create notifications with many different notification systems on Windows, Mac OS and Unix."
        self.defaultTarget = 'gitHEAD'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.staticDefine = "-DSNORE_STATIC=ON -DSNORE_STATIC_QT=ON"