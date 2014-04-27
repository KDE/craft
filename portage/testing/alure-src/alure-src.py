# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://repo.or.cz/alure.git'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['testing/openal-soft-src'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

