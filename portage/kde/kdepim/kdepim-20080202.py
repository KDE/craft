import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdepim'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdepim'
        self.targets['4.0.60'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.60/src/kdepim-4.0.60.tar.bz2'
        self.targetInstSrc['4.0.60'] = 'kdepim-4.0.60'        
        self.targets['4.0.61'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.61/src/kdepim-4.0.61.tar.bz2'
        self.targetInstSrc['4.0.61'] = 'kdepim-4.0.61'        
        self.targets['4.0.62'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.62/src/kdepim-4.0.62.tar.bz2'
        self.targetInstSrc['4.0.62'] = 'kdepim-4.0.62'        
        self.targets['4.0.63'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.63/src/kdepim-4.0.63.tar.bz2'
        self.targetInstSrc['4.0.63'] = 'kdepim-4.0.63'        
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['contributed/gpgme-qt'] = 'default'
        
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()
        self.kdeCustomDefines = "-DKLEO_BUILD_OLD_MAINWINDOW=1"
#        self.kdeCustomDefines += " -DBUILD_doc=OFF"

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdepim", self.buildTarget, True )
        else:
            return self.doPackaging( "kdepim", os.path.basename(sys.argv[0]).replace("kdepim-", "").replace(".py", ""), True )
		
if __name__ == '__main__':
    subclass().execute()
