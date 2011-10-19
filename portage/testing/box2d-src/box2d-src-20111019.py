# -*- coding: utf-8 -*-
import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'http://box2d.googlecode.com/svn/trunk/'
        self.targetConfigurePath['svnHEAD'] = 'Box2d'
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DBOX2D_INSTALL=ON -DBOX2D_BUILD_EXAMPLES=OFF"

if __name__ == '__main__':
    Package().execute()
