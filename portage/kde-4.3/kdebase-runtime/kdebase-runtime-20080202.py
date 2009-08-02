import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.3/kdebase/runtime'
        for ver in ['91', '95', '98']:
          self.targets['4.2.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.2.' + ver + '/src/kdebase-runtime-4.2.' + ver + '.tar.bz2'
          self.targetInstSrc['4.2.' + ver] = 'kdebase-runtime-4.2.' + ver
        for ver in ['0', '1', '2', '3', '4']:
          self.targets['4.3.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.3.' + ver + '/src/kdebase-runtime-4.3.' + ver + '.tar.bz2'
          self.targetInstSrc['4.3.' + ver] = 'kdebase-runtime-4.3.' + ver
        self.patchToApply['4.3.0'] = ( 'kdebase-ktimezoned.diff', 0 )
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.3/kdelibs'] = 'default'
        self.hardDependencies['kde-4.3/kdepimlibs'] = 'default'
        self.hardDependencies['kdesupport/oxygen-icons'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "runtime"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kde.buildTests=False
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdebase-runtime", self.buildTarget, True )
		
if __name__ == '__main__':
    subclass().execute()
