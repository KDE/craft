import base
import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdereview/step'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()
        self.instsrcdir = "step"
        
    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "step", "20080311", True )
		
if __name__ == '__main__':
    subclass().execute()
