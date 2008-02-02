import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdegraphics'
        self.targets['4.0.60'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.60/src/kdegraphics-4.0.60.tar.bz2'
        self.targetInstSrc['4.0.60'] = 'kdegraphics-4.0.60'        
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdegraphics'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase'] = 'default'
        self.hardDependencies['testing/poppler-src'] = 'default'
        
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        if self.traditional:
            self.instdestdir = "kde"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        if self.compiler == "mingw":
            self.kdeCustomDefines = "-DBUILD_kolourpaint=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdegraphics", os.path.basename(sys.argv[0]).replace("kdegraphics-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
