import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.1/kdeplasma-addons'
        for ver in ['0', '1', '2']:
          self.targets['4.1.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.1.' + ver + '/src/kdeplasma-addons-4.1.' + ver + '.tar.bz2'
          self.targetInstSrc['4.1.' + ver] = 'kdeplasma-addons-4.1.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.1/kdebase-runtime'] = 'default'
        self.hardDependencies['kde-4.1/kdebase-workspace'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        self.kdeCustomDefines = ""
        
        
    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdeplasma-addons", self.buildTarget, True )
        else:
            return self.doPackaging( "kdeplasma-addons", os.path.basename(sys.argv[0]).replace("kdeplasma-addons-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
