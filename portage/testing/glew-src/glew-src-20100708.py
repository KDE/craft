# -*- coding: utf-8 -*-
import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.5.4'] = 'http://downloads.sourceforge.net/project/glew/glew/1.5.4/glew-1.5.4.zip'
        self.targetInstSrc['1.5.4'] = 'glew-1.5.4'
        self.patchToApply['1.5.4'] = ('glew-1.5.4-20100708.diff', 1)
        self.options.package.withCompiler = False
        self.options.package.packageName = "glew"
        self.defaultTarget = '1.5.4'

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
