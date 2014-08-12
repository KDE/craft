# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.shortDescription = "A command line interface for libsnore"
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['kdesupport/snorenotify'] = 'default'



    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'https://github.com/Snorenotify/snore-send.git'
        self.defaultTarget = 'gitHEAD'


class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
