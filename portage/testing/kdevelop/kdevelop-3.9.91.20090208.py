# -*- coding: utf-8 -*-
import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdevelop'
        self.svnTargets['3.9.94'] = 'tags/kdevelop/3.9.94'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['testing/kdevplatform'] = 'default'
        self.hardDependencies['win32libs-bin/zip'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "kdevelop"
        self.subinfo = subinfo()

    def kdeSvnPath( self ):
        return "trunk/KDE/kdevelop"
        
    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()
    
    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdevelop", self.buildTarget, True )
        else:
            return self.doPackaging( "kdevelop" )

if __name__ == '__main__':
    subclass().execute()
