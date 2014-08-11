# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.shortDescription = "An application to show kde notifications with Snarl/Growl"
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['kde/ki18n'] = 'default'
        self.dependencies['kde/kiconthemes'] = 'default'
        self.dependencies['kde/kcoreaddons'] = 'default'



    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'https://github.com/Snorenotify/Snorenotify.git'
        for ver in ['0.2','0.3','0.4-beta1','0.4-beta2']:
            self.targets[ver] = 'https://github.com/TheOneRing/Snorenotify/archive/v%s.tar.gz' % ver
            self.archiveNames[ver] = "snorenotify-%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'Snorenotify-%s' % ver
        self.targetDigests['0.4-beta1'] = '76996e2ebd23fa7b99b68e743c880b3fa0d724af'
        self.defaultTarget = 'gitHEAD'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = '-DWITH_QT4=OFF -DWITH_FREEDESKTOP_FRONTEND=ON -DWITH_SNORE_DEAMON=ON '
        self.subinfo.options.fetch.checkoutSubmodules = True

