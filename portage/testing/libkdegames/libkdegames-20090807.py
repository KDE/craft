# -*- coding: utf-8 -*-
import info

from Package.CMakePackageBase import *
        
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "trunk/KDE/kdegames#norecursive;trunk/KDE/kdegames/libkdegames;trunk/KDE/kdegames/cmake"
        self.defaultTarget = 'svnHEAD'
        self.options.configure.configurePath = 'libkdegames'

    #def setDependencies( self ):
        #self.hardDependencies['kde/kdegames'] = 'default'
#        self.hardDependencies['testing/glew'] = 'default'


class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.onlyBuildTargets = "libkdegames"
            
if __name__ == '__main__':
    Package().execute()

    
