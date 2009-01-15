import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeedu/marble'
        self.svnTargets['0.5.1'] = 'branches/KDE/4.0/kdeedu/marble'
        self.svnTargets['0.6.1'] = 'branches/KDE/4.1/kdeedu/marble'
        self.svnTargets['0.7.1'] = 'branches/KDE/4.2/kdeedu/marble'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['libs/qt'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.subinfo = subinfo()
        self.kdeCustomDefines = "-DQTONLY=ON -DBUILD_MARBLE_TESTS=ON"
        
    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if not self.buildTarget == 'svnHEAD':
            return self.doPackaging( "marble", self.buildTarget, True )
        else:
            return self.doPackaging( "marble", os.path.basename(sys.argv[0]).replace("marble-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
