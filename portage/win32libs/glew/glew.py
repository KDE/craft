# -*- coding: utf-8 -*-
import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.5.4', '1.7.0', '1.9.0', '1.10.0']:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/project/glew/glew/' + ver + '/glew-'+ ver + '.zip'
            self.targetInstSrc[ ver ] = 'glew-' + ver
        self.patchToApply['1.5.4'] = [('glew-1.5.4-20100708.diff', 1)]
        self.patchToApply['1.7.0'] = [('glew-1.7.0-20120320.diff', 1)]
        self.patchToApply['1.9.0'] = [('glew-1.9.0-20130124.diff', 1)]
        self.patchToApply['1.10.0'] = [('glew-1.9.0-20130124.diff', 1)]
        self.targetDigests['1.7.0'] = '107c155ff5b69d97b9c530b40e4e8da571aaf729'
        self.targetDigests['1.9.0'] = '6c0dd8d6af14db93868bb5482b55e784b2dc1127'
        self.targetDigests['1.10.0'] = 'da45a883ca9b2a8e8fc1a642bd043f251ad69151'

        self.shortDescription = "OpenGL Extension Wrangler Library"
        self.defaultTarget = '1.10.0'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)

