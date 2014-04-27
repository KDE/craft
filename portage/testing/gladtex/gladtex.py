# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "https://svn.code.sf.net/p/gladtex/code/trunk"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/giflib'] = 'default'
        self.dependencies['win32libs/libpng'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()