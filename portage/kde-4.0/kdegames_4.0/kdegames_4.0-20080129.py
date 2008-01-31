import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdegames'
        self.svnTargets['4.0.1'] = 'tags/KDE/4.0.1/kdegames'
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.0/kdegames'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.0/kdebase_4.0'] = 'default'
        
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "kdegames"
        self.subinfo = subinfo()

    def unpack( self ):
        self.kdeSvnUnpack()
        return True

    def compile( self ):
        return self.kdeCompile()
    
    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdegames", os.path.basename(sys.argv[0]).replace("kdegames-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
