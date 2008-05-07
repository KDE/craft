import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdebase/runtime'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdebase/runtime'
        for ver in ['70', '71', '72', '73']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdebase-runtime-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdebase-runtime-4.0.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kde/kdepimlibs'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "runtime"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdebase-runtime", self.buildTarget, True )
        else:
            return self.doPackaging( "kdebase-runtime", os.path.basename(sys.argv[0]).replace("kdebase-runtime-", "").replace(".py", ""), True )

		
if __name__ == '__main__':
    subclass().execute()
