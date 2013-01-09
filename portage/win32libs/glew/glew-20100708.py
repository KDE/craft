# -*- coding: utf-8 -*-
import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.5.4', '1.7.0']:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/project/glew/glew/' + ver + '/glew-'+ ver + '.zip'
            self.targetInstSrc[ ver ] = 'glew-' + ver
        self.patchToApply['1.5.4'] = ('glew-1.5.4-20100708.diff', 1)
        self.patchToApply['1.7.0'] = ('glew-1.7.0-20120320.diff', 1)
        self.targetDigests['1.7.0'] = '107c155ff5b69d97b9c530b40e4e8da571aaf729'
        self.defaultTarget = '1.7.0'

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
