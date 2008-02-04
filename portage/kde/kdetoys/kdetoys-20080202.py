import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdetoys'
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdetoys'
        self.targets['4.0.60'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.60/src/kdetoys-4.0.60.tar.bz2'
        self.targetInstSrc['4.0.60'] = 'kdetoys-4.0.60'
        self.defaultTarget = '4.0.60'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        
class subclass(base.baseclass):
    def __init__(self):
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
            return self.doPackaging( "kdetoys", self.buildTarget, True )
        else:
            return self.doPackaging( "kdetoys", os.path.basename(sys.argv[0]).replace("kdetoys-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
