# -*- coding: utf-8 -*-
import info

from Source.SvnSource import *
from BuildSystem.CMakeBuildSystem import *
from Package.PackageBase import *
from Packager.KDEWinPackager import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "trunk/playground/games"
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
        defines = ""
        defines += " -DBUILD_doc=OFF"
        defines += " -DBUILD_libksirtet=OFF"
        defines += " -DBUILD_kbackgammon=OFF"
        defines += " -DBUILD_kigo=OFF"
        defines += " -DBUILD_kolf-ng=ON"
        defines += " -DBUILD_kombination=OFF"
        defines += " -DBUILD_ksimili=OFF"
        defines += " -DBUILD_ksirtet=OFF"
        defines += " -DBUILD_kttt=OFF"
        defines += " -DBUILD_magazynier=OFF"
        defines += " -DBUILD_palapeli=OFF"
        defines += " -DBUILD_pege=OFF"
        defines += " -DBUILD_superpong=OFF"
        defines += " -DBUILD_kamala=OFF"
        defines += " -DBUILD_astrododge=OFF"
        defines += " -DBUILD_draughts=OFF"
        defines += " -DBUILD_kollagame=OFF"
        defines += " -DBUILD_kpicross=OFF"
        defines += " -DBUILD_kpoker=OFF"
        defines += " -DBUILD_ktank=OFF"
        defines += " -DBUILD_market=OFF"
        defines += " -DBUILD_nonogram=OFF"
        defines += " -DBUILD_parsek=OFF"
        defines += " -DBUILD_mancala=OFF"
        self.subinfo.options.configure.defines = defines
        
if __name__ == '__main__':
    Package().execute()
