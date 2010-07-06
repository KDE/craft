# -*- coding: utf-8 -*-
import utils
import os
import info
import platform
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://git.gnupg.org/pinentry-qt.git'
        self.targetSrcSuffix['gitHEAD'] = 'git'

        self.defaultTarget = 'gitHEAD'
        
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

from Package.CMakePackageBase import *
                
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
    
if __name__ == '__main__':
    Package().execute()
