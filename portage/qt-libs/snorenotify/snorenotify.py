# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['dev-util/extra-cmake-modules'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtquick1'] = 'default'
        self.dependencies['libs/qttools'] = 'default'
        self.dependencies['win32libs/snoregrowl'] = 'default'



    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:snorenotify'
        for ver in ['0.5.1', '0.5.2', '0.5.3']:
            self.targets[ver] = 'https://github.com/Snorenotify/Snorenotify/archive/v%s.tar.gz' % ver
            self.archiveNames[ver] = "snorenotify-%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'Snorenotify-%s' % ver
        self.targetDigests['0.5.1'] = 'eb83e0b7bccfc1c307a8457265dc4a5607a8b877'
        self.targetDigests['0.5.2'] = '9aa4409422872dd32bd5f831a6201820994065a1'
        self.targetDigests['0.5.3'] = '542991b86ac0124e4f8d7ffec7783a2449f655f3'
        self.shortDescription = "Snorenotify is a multi platform Qt notification framework. Using a plugin system it is possible to create notifications with many different notification systems on Windows, Mac OS and Unix."
        self.defaultTarget = 'gitHEAD'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = ''
        if self.buildTarget.startswith("0.5"):
            if self.subinfo.options.isActive("win32libs/dbus"):
                self.subinfo.options.configure.defines += '-DWITH_FREEDESKTOP_FRONTEND=ON '
            self.subinfo.options.configure.defines += '-DWITH_FRONTENDS=ON -DWITH_SNORE_DAEMON=ON '
            self.subinfo.options.configure.defines += "-DWITH_QT4=OFF "

