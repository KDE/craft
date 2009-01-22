import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.2/kdeutils'
        for ver in ['0']:
          self.targets['4.2.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.2.' + ver + '/src/kdeutils-4.2.' + ver + '.tar.bz2'
          self.targetInstSrc['4.2.' + ver] = 'kdeutils-4.2.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.2/kdebase-runtime'] = 'default'
        self.hardDependencies['win32libs-sources/libgmp-src'] = 'default'

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
        return self.doPackaging( "kdeutils", self.buildTarget, True )

if __name__ == '__main__':
    subclass().execute()
