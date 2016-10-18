# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues(  )

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies["win32libs/llvm"] = "default"

from Package.SourceOnlyPackageBase import *

class Package(SourceOnlyPackageBase):
    def __init__( self, **args ):
        SourceOnlyPackageBase.__init__(self)

