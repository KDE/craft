# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['qt-apps/libaccu'] = 'default'
        self.dependencies['qt-libs/snorenotify'] = 'default'

        
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/qewitter/qewitter.git'
        self.defaultTarget = 'gitHEAD'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        #self.subinfo.options.cmake.openIDE = True

