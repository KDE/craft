# -*- coding: utf-8 -*-
import base
import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for i in ( '0.10.1', '0.10.2', '0.10.3', '0.10.4', '0.10.5', '0.10.6' ):
          self.targets[ i ] = 'http://poppler.freedesktop.org/poppler-%s.tar.gz' % i
          self.targetInstSrc[ i ] = 'poppler-%s' % i
        self.defaultTarget = "0.10.6"
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/fontconfig'] = 'default'
        self.hardDependencies['win32libs-bin/freetype'] = 'default'
        self.hardDependencies['data/poppler-data'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
        return True
        
        
    def compile( self ):
        self.kdeCustomDefines = "-DBUILD_QT4_TESTS=ON"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def kdeSvnPath( self ):
        return False
        
    def make_package( self ):
        self.doPackaging( "poppler", self.buildTarget, True )
        return True

if __name__ == '__main__':
    subclass().execute()
