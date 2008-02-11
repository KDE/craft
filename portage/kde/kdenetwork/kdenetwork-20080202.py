import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdenetwork'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdenetwork'
        self.targets['4.0.60'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.60/src/kdenetwork-4.0.60.tar.bz2'
        self.targetInstSrc['4.0.60'] = 'kdenetwork-4.0.60'
        self.targets['4.0.61'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.61/src/kdenetwork-4.0.61.tar.bz2'
        self.targetInstSrc['4.0.61'] = 'kdenetwork-4.0.61'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.softDependencies['kdesupport/qca'] = 'default'
        
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
            return self.doPackaging( "kdenetwork", self.buildTarget, True )
        else:
            return self.doPackaging( "kdenetwork", os.path.basename(sys.argv[0]).replace("kdenetwork-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
