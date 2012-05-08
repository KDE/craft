# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['3.1.1']:
            self.targets[ ver ] = "http://www.apache.org/dist/xerces/c/3/sources/xerces-c-" + ver + ".tar.gz"
            self.targetInstSrc[ ver ] = "xerces-c-" + ver
        self.patchToApply['3.1.1'] = [("xerces-c-3.1.1-20120507.diff", 1)]
        self.targetDigests['3.1.1'] = '177ec838c5119df57ec77eddec9a29f7e754c8b2'
        self.shortDescription = "a validating XML parser written in a portable subset of C++"
        self.defaultTarget = '3.1.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()