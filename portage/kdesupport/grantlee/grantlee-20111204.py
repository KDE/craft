# -*- coding: utf-8 -*-
import info
import emergePlatform

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "git://gitorious.org/grantlee/grantlee.git"
        for ver in ['0.1', '0.2', '0.3']:
            self.svnTargets[ ver ] = "git://gitorious.org/grantlee/grantlee.git|%s" % ver
        for ver in ['0.3.0']:
            self.targets[ ver ] = "http://downloads.grantlee.org/grantlee-%s.tar.gz" % ver
            self.targetInstSrc[ ver ] = "grantlee-%s" % ver
        self.patchToApply['0.3.0'] = [("0001-add-plugin-path-depending-on-executable-location.patch", 1),
                                      ("patches/0.3.0/fix-exports-generator-for-intel-compiler.diff", 1)]

        self.shortDescription = 'libraries for a template system similar to django\'s'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'

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
