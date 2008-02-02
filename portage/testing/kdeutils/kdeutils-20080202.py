import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeutils'
        self.targets['4.0.60'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.60/src/kdeutils-4.0.60.tar.bz2'
        self.targetInstSrc['4.0.60'] = 'kdeutils-4.0.60'        
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kde/kdepimlibs'] = 'default'
        self.hardDependencies['kde/kdebase'] = 'default'
    
class subclass(base.baseclass):
    def __init__(self):
        self.buildType="Debug"
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()
#        self.kdeCustomDefines = "-DBUILD_kwallet=OFF"
        self.kdeCustomDefines = "-DBUILD_doc=OFF"

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdeutils", self.buildTarget, True )
        else:
            return self.doPackaging( "kdeutils", os.path.basename(sys.argv[0]).replace("kdeutils-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
