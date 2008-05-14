import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdepimlibs'
        self.svnTargets['4.0.1'] = 'tags/KDE/4.0.1/kdepimlibs'
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.0/kdepimlibs'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.0/kdelibs_4.0'] = 'default'
        self.softDependencies['contributed/gpgme-qt'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "kdepimlibs"
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
        return self.doPackaging( "kdepimlibs", os.path.basename(sys.argv[0]).replace("kdepimlibs_4.0-", "").replace(".py", ""), True )


if __name__ == '__main__':
    subclass().execute()
