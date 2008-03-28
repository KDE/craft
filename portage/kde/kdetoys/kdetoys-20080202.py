import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdetoys'
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdetoys'
        for ver in ['65', '66', '67']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdetoys-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdetoys-4.0.' + ver
        self.defaultTarget = 'svnHEAD'
    
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
