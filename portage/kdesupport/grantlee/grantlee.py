# -*- coding: utf-8 -*-
import info


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
        self.targetDigests['0.3.0'] = 'dbfd4370d48f10731b638a73abc848bb25602a35'
        self.shortDescription = 'libraries for a template system similar to django\'s'
        self.defaultTarget = '0.3.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = '-DBUILD_TESTS=OFF'

