import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdepimlibs'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdepimlibs'
        self.targets['4.0.60'] = 'ftp://ftp.rz.uni-wuerzburg.de/pub/unix/kde/unstable/4.0.60/src/kdepimlibs-4.0.60.tar.bz2'
        self.targetInstSrc['4.0.60'] = 'kdepimlibs-4.0.60'        
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.softDependencies['contributed/gpgme-qt'] = 'default'
        
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
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
        return self.doPackaging( "kdepimlibs", os.path.basename(sys.argv[0]).replace("kdepimlibs-", "").replace(".py", ""), True )


if __name__ == '__main__':
    subclass().execute()
