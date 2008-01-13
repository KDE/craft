import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdevelop'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['testing/kdevplatform'] = 'default'
    
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "kdevelop"
        self.subinfo = subinfo()

    def kdeSvnPath( self ):
        return "trunk/KDE/kdevelop"
        
    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()
    
    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "kdevelop", os.path.basename(sys.argv[0]).replace("kdevelop-", "").replace(".py", ""), True )

if __name__ == '__main__':
    subclass().execute()
