import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdegames'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdegames'
        self.targets['4.0.61'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.61/src/kdegames-4.0.61.tar.bz2'
        self.targetInstSrc['4.0.61'] = 'kdegames-4.0.61'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()

    def unpack( self ):
        self.kdeSvnUnpack()
        return True

    def compile( self ):
        return self.kdeCompile()
    
    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdegames", self.buildTarget, True )
        else:
            return self.doPackaging( "kdegames", os.path.basename(sys.argv[0]).replace("kdegames-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
