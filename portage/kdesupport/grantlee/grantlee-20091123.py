# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['0.1'] = "git://gitorious.org/grantlee/grantlee.git"
        self.defaultTarget = '0.1'
        self.options.package.withCompiler = False

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        if self.buildTarget == '0.1':
            self.subinfo.options.package.withCompiler = True

        
if __name__ == '__main__':
    Package().execute()
