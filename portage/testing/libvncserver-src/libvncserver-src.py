# -*- coding: utf-8 -*-
import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.9.8.2'] = 'http://downloads.sourceforge.net/project/libvncserver/libvncserver/0.9.8.2/LibVNCServer-0.9.8.2.tar.gz'
        self.targetInstSrc['0.9.8.2'] = 'LibVNCServer-0.9.8.2'
        self.patchToApply['0.9.8.2'] = ('libvncserver-0.9.8.2-build-fixes.diff', 1)
        self.options.package.packageName = "libvncserver"
        self.defaultTarget = '0.9.8.2'

    def setDependencies( self ):
        self.dependencies['virtual/bin-base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)


