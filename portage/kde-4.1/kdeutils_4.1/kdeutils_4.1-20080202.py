import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.1/kdeutils'
        for ver in ['0']:
          self.targets['4.1.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.1.' + ver + '/src/kdeutils-4.1.' + ver + '.tar.bz2'
          self.targetInstSrc['4.1.' + ver] = 'kdeedu-4.1.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.1/kdebase-runtime_4.1'] = 'default'

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
            return self.doPackaging( "kdeutils", self.buildTarget, True )
        else:
            return self.doPackaging( "kdeutils", os.path.basename(sys.argv[0]).replace("kdeutils-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
