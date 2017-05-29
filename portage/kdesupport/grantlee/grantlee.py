# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['master'] = "https://github.com/steveire/grantlee.git"
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        CMakePackageBase.__init__(self)
