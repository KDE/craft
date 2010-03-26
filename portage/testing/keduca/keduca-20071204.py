import base
import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "trunk/playground/edu/keduca"
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdeedu'] = 'default'
    

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "keduca"

    def kdeSvnPath( self ):
        return "trunk/playground/edu/keduca"

    def unpack( self ):
        unp = self.kdeSvnUnpack()
        # now copy the tree to workdir
        return unp


    def kdeDefaultDefines( self ):
        options = base.baseclass.kdeDefaultDefines( self )
        return options

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "keduca", "20070412", True )
		
if __name__ == '__main__':
    subclass().execute()
