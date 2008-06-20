import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeutils'
        for ver in ['74', '80', '83']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdeutils-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdeutils-enterprise4-4.0.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['contributed/kdebase-runtime-branch'] = 'default'

class subclass(base.baseclass):
    def __init__( self, **args ):
        self.buildType="Debug"
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        self.kdeCustomDefines = ""
#        self.kdeCustomDefines += "-DBUILD_kwallet=OFF "
#        self.kdeCustomDefines += "-DBUILD_doc=OFF"

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdeutils-enterprise4", self.buildTarget, True )
        else:
            return self.doPackaging( "kdeutils-enterprise4", os.path.basename(sys.argv[0]).replace("kdeutils-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
