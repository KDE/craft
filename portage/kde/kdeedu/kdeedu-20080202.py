import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdeedu'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeedu'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdeedu-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdeedu-4.0.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'

        self.softDependencies['kdesupport/eigen'] = 'default'
        self.softDependencies['kdesupport/gmm'] = 'default'
        self.hardDependencies['win32libs-bin/cfitsio'] = 'default'
        self.hardDependencies['win32libs-bin/libnova'] = 'default'
        self.hardDependencies['win32libs-bin/openbabel'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "kdeedu"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        self.kdeCustomDefines = "-DBUILD_doc=OFF"
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdeedu", self.buildTarget, True )
        else:
            return self.doPackaging( "kdeedu" )

if __name__ == '__main__':
    subclass().execute()
