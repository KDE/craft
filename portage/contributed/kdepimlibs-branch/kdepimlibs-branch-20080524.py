import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/kdepim/enterprise4/kdepimlibs'
        for ver in ['74', '80', '83']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdepimlibs-enterprise4-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdepimlibs-enterprise4-4.0.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['contributed/kdelibs-branch'] = 'default'
#        self.hardDependencies['contributed/gpgme-qt'] = 'default'
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
            return self.doPackaging( "kdepimlibs-enterprise4", self.buildTarget, True )
        else:
            return self.doPackaging( "kdepimlibs-enterprise4", os.path.basename(sys.argv[0]).replace("kdepimlibs-", "").replace(".py", ""), True )


if __name__ == '__main__':
    subclass().execute()
