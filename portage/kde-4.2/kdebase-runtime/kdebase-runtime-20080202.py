import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.2/kdebase/runtime'
        for ver in ['0']:
          self.targets['4.2.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.2.' + ver + '/src/kdebase-runtime-4.2.' + ver + '.tar.bz2'
          self.targetInstSrc['4.2.' + ver] = 'kdebase-runtime-4.2.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.2/kdelibs'] = 'default'
        self.hardDependencies['kde-4.2/kdepimlibs'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "runtime"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack():

    def compile( self ):
        self.kde.buildTests=False
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdebase-runtime", self.buildTarget, True )
		
if __name__ == '__main__':
    subclass().execute()
