# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.shortDescription = "A command line interface for libsnore"
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['qt-libs/snorenotify'] = 'default'



    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'https://github.com/Snorenotify/snore-send.git'
        self.svnTargets['0.5'] = 'https://github.com/Snorenotify/snore-send.git|0.5'
        self.defaultTarget = 'gitHEAD'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
