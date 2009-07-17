# -*- coding: utf-8 -*-
import base
import os
import sys
import info
import utils

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/graphics/kphotoalbum'
        
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdegraphics'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        #self.instsrcdir = "kphotoalbum"
        self.subinfo = subinfo()

    def unpack( self ):
            return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kphotoalbum" )
        else:
            return self.doPackaging( "kphotoalbum", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
