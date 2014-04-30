# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://github.com/JonathanBeck/libplist.git'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['win32libs/libxml2'] = 'default'
        self.dependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

