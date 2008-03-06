import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdegraphics'
        for ver in ['61', '62', '63', '64', '65']:
          self.targets['4.0.' + ver] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.' + ver + '/src/kdegraphics-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdegraphics-4.0.' + ver
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdegraphics'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
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
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdegraphics", self.buildTarget, True )
        else:
            return self.doPackaging( "kdegraphics", os.path.basename(sys.argv[0]).replace("kdegraphics-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
