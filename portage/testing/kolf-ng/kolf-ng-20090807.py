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
        
        defines = ""
        defines += " -DBUILD_doc=OFF"
        defines += " -DBUILD_libksirtet=OFF"
        defines += " -DBUILD_kbackgammon=OFF"
        defines += " -DBUILD_kigo=OFF"
#        defines += " -DBUILD_kolf-ng=OFF"
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
