import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.1/kdepim'
        for ver in ['0', '1', '2', '3']:
          self.targets['4.1.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.1.' + ver + '/src/kdepim-4.1.' + ver + '.tar.bz2'
          self.targetInstSrc['4.1.' + ver] = 'kdepim-4.1.' + ver
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde-4.1/kdebase-runtime-branch'] = 'default'
        self.hardDependencies['win32libs-bin/sqlite'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        self.kdeCustomDefines = "-DKLEO_SYNCHRONOUS_API_HOTFIX=ON"
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
