# -*- coding: utf-8 -*-
import utils
import os
import info
import platform
import compiler

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://cvs.gnupg.org/wincetools.git'
        self.svnTargets['kdepimcetools'] = \
                'git://cvs.gnupg.org/wincetools.git|kdepimcetools|'
        self.targetConfigurePath['gitHEAD'] = 'loader'
        self.targetConfigurePath['kdepimcetools'] = 'loader'
        self.defaultTarget = 'kdepimcetools'
        
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *
                
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
    
if __name__ == '__main__':
    Package().execute()
