import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdebindings'
        self.targets['4.0.60'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.60/src/kdebindings-4.0.60.tar.bz2'
        self.targetInstSrc['4.0.60'] = 'kdebindings-4.0.60'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        self.kdeCustomDefines = ""
        
        
    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = "-DBUILD_csharp=OFF"
        self.kdeCustomDefines += " -DBUILD_java=OFF"
        self.kdeCustomDefines += " -DBUILD_kalyptus=OFF"
        self.kdeCustomDefines += " -DBUILD_php=OFF"
        self.kdeCustomDefines += " -DBUILD_ruby=OFF"
        self.kdeCustomDefines += " -DBUILD_smoke=OFF"
        self.kdeCustomDefines += " -DBUILD_xparts=OFF"
        self.kdeCustomDefines += " -DBUILD_PYKDE4=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdebindings", self.buildTarget, True )
        else:
            return self.doPackaging( "kdebindings", os.path.basename(sys.argv[0]).replace("kdebindings-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
