# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://git.gnupg.org/pinentry-qt.git'
        self.targetSrcSuffix['gitHEAD'] = 'git'

        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

