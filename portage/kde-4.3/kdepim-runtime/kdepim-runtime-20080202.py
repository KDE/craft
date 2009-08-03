import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['0', '1', '2', '3', '4']:
          self.targets['4.3.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.3.' + ver + '/src/kdepim-runtime-4.3.' + ver + '.tar.bz2'
          self.targetInstSrc['4.3.' + ver] = 'kdepim-runtime-4.3.' + ver
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde-4.3/kdebase-runtime'] = 'default'
        self.hardDependencies['win32libs-bin/sqlite'] = 'default'
        
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
        return self.doPackaging( "kdepim-runtime", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
