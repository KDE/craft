# -*- coding: utf-8 -*-
import info
import emergePlatform

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://gitorious.org/grantlee/grantlee.git"
        for ver in ['0.1', '0.2', '0.3']:
            self.svnTargets[ ver ] = "git://gitorious.org/grantlee/grantlee.git|%s" % ver
        self.shortDescription = 'libraries for a template system similar to django\'s'
        self.defaultTarget = '0.3'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qt'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        if not emergePlatform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines = '-DBUILD_TESTS=OFF'
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
