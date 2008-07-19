import base
import utils
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdebase'
        self.svnTargets['4.0.1'] = 'tags/KDE/4.0.1/kdebase'
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.0/kdebase'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.0/kdelibs'] = 'default'
        self.hardDependencies['kde-4.0/kdepimlibs'] = 'default'
    
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "kdebase"
        self.subinfo = subinfo()

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdebase", utils.cleanPackageName( sys.argv[0], "kdebase" ), True )

		
if __name__ == '__main__':
    subclass().execute()
