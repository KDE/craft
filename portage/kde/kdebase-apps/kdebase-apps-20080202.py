import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdebase/apps'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdebase/apps'
        self.targets['4.0.60'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.60/src/kdebase-4.0.60.tar.bz2'
        self.targetInstSrc['4.0.60'] = 'kdebase-4.0.60'        
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kde/kdepimlibs'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdebase-apps", self.buildTarget, True )
        else:
            return self.doPackaging( "kdebase-apps", os.path.basename(sys.argv[0]).replace("kdebase-apps-", "").replace(".py", ""), True )

		
if __name__ == '__main__':
    subclass().execute()
