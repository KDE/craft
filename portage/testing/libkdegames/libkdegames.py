# -*- coding: utf-8 -*-
import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "trunk/KDE/kdegames#norecursive;trunk/KDE/kdegames/libkdegames#main;trunk/KDE/kdegames/cmake"
        self.defaultTarget = 'svnHEAD'
        self.options.configure.configurePath = 'libkdegames'

    #def setDependencies( self ):
        #self.dependencies['kde/kdegames'] = 'default'
#        self.dependencies['testing/glew'] = 'default'


class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.onlyBuildTargets = "libkdegames"



