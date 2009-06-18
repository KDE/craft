import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/kdepim/enterprise4/kdepim'
        for ver in ['74', '80', '83']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdepim-enterprise4-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdepim-enterprise4-4.0.' + ver
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['contributed/kdebase-runtime-branch'] = 'default'
#        self.hardDependencies['contributed/gpgme-qt'] = 'default'
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
            return self.doPackaging( "kdepim-enterprise4", self.buildTarget, True )
        else:
            return self.doPackaging( "kdepim-enterprise4", os.path.basename(sys.argv[0]).replace("kdepim-", "").replace(".py", ""), True )
		
if __name__ == '__main__':
    subclass().execute()
