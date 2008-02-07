import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeedu/marble'
        self.svnTargets['0.5.1'] = 'branches/KDE/4.0/kdeedu/marble'
        self.defaultTarget = '0.5.1'
    
    def setDependencies( self ):
        self.hardDependencies['libs/qt'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()
        self.kdeCustomDefines = "-DQTONLY=ON"
        
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
