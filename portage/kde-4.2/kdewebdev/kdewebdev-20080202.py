import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.2/kdewebdev'
        for ver in ['0', '1', '2', '3', '4']:
          self.targets['4.2.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.2.' + ver + '/src/kdewebdev-4.2.' + ver + '.tar.bz2'
          self.targetInstSrc['4.2.' + ver] = 'kdewebdev-4.2.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.2/kdebase-runtime'] = 'default'
        self.softDependencies['kde-4.2/kdevplatform'] = 'default'
        
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
        return self.doPackaging( "kdewebdev", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
