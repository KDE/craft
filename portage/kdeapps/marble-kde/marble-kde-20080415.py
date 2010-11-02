# -*- coding: utf-8 -*-
import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeedu/marble'
        self.svnTargets['4.2'] = 'branches/KDE/4.2/kdeedu/marble'
        self.svnTargets['4.3'] = 'branches/KDE/4.3/kdeedu/marble'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
#        self.hardDependencies['kde-4.3/kdebase-runtime'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "kdeedu"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = ""
        self.kdeCustomDefines += " -DTILES_AT_COMPILETIME=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def unittest( self ):
        return self.kdeTest()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "marble-kde", self.buildTarget, True )
        else:
            return self.doPackaging( "marble-kde", os.path.basename(sys.argv[0]).replace("marble-kde-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
