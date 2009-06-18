import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdepimlibs'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdepimlibs'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdepimlibs-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdepimlibs-4.0.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['win32libs-bin/libical'] = 'default'
        self.hardDependencies['win32libs-bin/gpgme'] = 'default'
        self.hardDependencies['win32libs-bin/cyrus-sasl'] = 'default'
        self.hardDependencies['kdesupport/akonadi'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        # add env var so that boost headers are found
        path = os.path.join( self.rootdir, "win32libs" )
        os.putenv( "BOOST_ROOT", path )

        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "kdepimlibs", self.buildTarget, True )
        else:
            return self.doPackaging( "kdepimlibs" )


if __name__ == '__main__':
    subclass().execute()
