# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['dev-util/extra-cmake-modules'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtquick1'] = 'default'
        self.dependencies['libs/qttools'] = 'default'
        self.dependencies['libs/qtwebsockets'] = 'default'
        self.dependencies['libs/qtmultimedia'] = 'default'
        self.dependencies['win32libs/snoregrowl'] = 'default'



    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:snorenotify'
        for ver in ['0.6.0']:
            self.targets[ ver ] = "http://download.kde.org/stable/snorenotify/src/%s/snorenotify-%s.tar.xz" % ( ver ,ver )
            self.targetInstSrc[ ver ] = "snorenotify-%s" % ver
        self.targetDigests['0.6.0'] = 'f2c28962ba6548829ba50c906b95068d3ef7aa1f'

        self.shortDescription = "Snorenotify is a multi platform Qt notification framework. Using a plugin system it is possible to create notifications with many different notification systems on Windows, Mac OS and Unix."
        self.defaultTarget = '0.6.0'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)