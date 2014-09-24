# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['dev-util/extra-cmake-modules'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtquick1'] = 'default'
        self.dependencies['win32libs/snoregrowl'] = 'default'



    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'https://github.com/Snorenotify/Snorenotify.git'
        for ver in ['0.5.1']:
            self.targets[ver] = 'https://github.com/TheOneRing/Snorenotify/archive/v%s.tar.gz' % ver
            self.archiveNames[ver] = "snorenotify-%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'Snorenotify-%s' % ver
        self.targetDigests['0.5.1'] = 'eb83e0b7bccfc1c307a8457265dc4a5607a8b877'
        self.shortDescription = "An application to show kde notifications with Win8, Snarl or Growl"
        self.defaultTarget = '0.5.1'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = '-DWITH_QT4=OFF -DWITH_FREEDESKTOP_FRONTEND=ON -DWITH_FRONTENDS=ON -DWITH_SNORE_DEAMON=ON '
        self.subinfo.options.fetch.checkoutSubmodules = True

