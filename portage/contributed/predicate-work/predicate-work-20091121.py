# -*- coding: utf-8 -*-
# Predicate work branch with kdelibs and kdelibs trunk
import base
import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "branches/work/predicate"
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdepimlibs'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "predicate"
        self.subinfo = subinfo()
        self.kdeCustomDefines = ""

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "predicate" )

if __name__ == '__main__':
    subclass().execute()
