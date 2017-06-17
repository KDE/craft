# -*- coding: utf-8 -*-
import info
import portage

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( packageName = "cfe", gitUrl = "[git]http://llvm.org/git/clang.git")


    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/libxml2'] = 'default'
        self.dependencies['win32libs/llvm'] = 'default'

from Package.SourceOnlyPackageBase import *

class Package(SourceOnlyPackageBase):
    def __init__( self, **args ):
        SourceOnlyPackageBase.__init__(self)
