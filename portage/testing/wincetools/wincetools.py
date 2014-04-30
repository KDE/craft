# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://cvs.gnupg.org/wincetools.git'
        self.svnTargets['kdepimcetools'] = \
                'git://cvs.gnupg.org/wincetools.git|kdepimcetools|'
        self.targetConfigurePath['gitHEAD'] = 'loader'
        self.targetConfigurePath['kdepimcetools'] = 'loader'
        self.defaultTarget = 'kdepimcetools'

    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

