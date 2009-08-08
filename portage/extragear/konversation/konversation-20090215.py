# -*- coding: utf-8 -*-
import base
import os
import utils
import info
import sys

class subinfo(info.infoclass):
    def setTargets( self ):
        for i in ['1', '2', '3', '5', '6']:
            self.targets['1.2alpha' + i] = 'http://download2.berlios.de/konversation/konversation-1.2-alpha' + i + '.tar.bz2'
            self.targetInstSrc['1.2alpha' + i] = 'konversation-1.2-alpha' + i
        self.svnTargets['svnHEAD'] = 'trunk/extragear/network/konversation'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kdesupport/qca'] = 'default'
        self.hardDependencies['kde/kdepimlibs'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "konversation", self.buildTarget, True )
        else:
            return self.doPackaging( "konversation" )
		
if __name__ == '__main__':
    subclass().execute()
