import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.1'] = 'branches/kdepim/enterprise4/kdebase-4.1-branch/runtime'
        self.svnTargets['4.2'] = 'branches/kdepim/enterprise4/kdebase-4.2-branch/runtime'
        for ver in ['74', '80', '83']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdebase-runtime-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdebase-runtime-enterprise4-4.0.' + ver
        self.defaultTarget = '4.1'
    
    def setDependencies( self ):
        if self.buildTarget == '4.1':
            self.hardDependencies['contributed/kdelibs-branch'] = '4.1'
        else:
            self.hardDependencies['contributed/kdelibs-branch'] = '4.2'
        self.hardDependencies['contributed/kdepimlibs-branch'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "runtime"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kde.buildTests=False
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdebase-runtime-enterprise4", self.buildTarget, True )
        else:
            return self.doPackaging( "kdebase-runtime-enterprise4", os.path.basename(sys.argv[0]).replace("kdebase-runtime-", "").replace(".py", ""), True )

		
if __name__ == '__main__':
    subclass().execute()
