# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['qt-apps/libaccu'] = 'default'
        self.hardDependencies['kdesupport/snorenotify'] = 'default'

        
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/qewitter/qewitter.git'
        self.defaultTarget = 'gitHEAD'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        #self.subinfo.options.cmake.openIDE = True

if __name__ == '__main__':
    Package().execute()
