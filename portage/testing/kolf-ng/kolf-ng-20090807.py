# -*- coding: utf-8 -*-
import info

from Source.SvnSource import *
from BuildSystem.CMakeBuildSystem import *
from Package.PackageBase import *
from Packager.KDEWinPackager import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "trunk/playground/games/kolf-ng"
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde/kdegames'] = 'default'

class Package(PackageBase, SvnSource, CMakeBuildSystem, KDEWinPackager):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        SvnSource.__init__(self)
        CMakeBuildSystem.__init__(self)
        PackageBase.__init__(self)
        KDEWinPackager.__init__(self)
        
if __name__ == '__main__':
    Package().execute()
