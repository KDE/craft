import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.2/kdetoys'
        for ver in ['80']:
          self.targets['4.1.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.1.' + ver + '/src/kdetoys-4.1.' + ver + '.tar.bz2'
          self.targetInstSrc['4.1.' + ver] = 'kdetoys-4.1.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.2/kdebase-runtime'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
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
