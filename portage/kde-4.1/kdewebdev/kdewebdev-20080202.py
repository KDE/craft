import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.1/kdewebdev'
        for ver in ['0', '1', '2', '3']:
          self.targets['4.1.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.1.' + ver + '/src/kdewebdev-4.1.' + ver + '.tar.bz2'
          self.targetInstSrc['4.1.' + ver] = 'kdewebdev-4.1.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.1/kdebase-runtime'] = 'default'
        self.softDependencies['kde-4.1/kdevplatform'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        # if you want to build quanta, you need to build kdevplatform as well - this is not build by default!!!
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_quanta=OFF "
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kfilereplace=OFF "
        self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kxsldbg=OFF "
	self.kdeCustomDefines = self.kdeCustomDefines + "-DBUILD_kommander=OFF "

        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdewebdev", self.buildTarget, True )
        else:
            return self.doPackaging( "kdewebdev", os.path.basename(sys.argv[0]).replace("kdewebdev-", "").replace(".py", ""), True )


if __name__ == '__main__':
    subclass().execute()
