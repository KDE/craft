# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "trunk/playground/games#norecursive;trunk/playground/games/cmake;trunk/playground/games/kolf-ng"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde/kdegames'] = 'default'
        self.hardDependencies['testing/glew'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.onlyBuildTargets = 'kolf-ng'

if __name__ == '__main__':
    Package().execute()
