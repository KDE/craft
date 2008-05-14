import base
import os
import utils

DEPEND = """
kde/kdelibs
contributed/kdepimlibs-branch
kde/kdebase
"""

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "kdepim"

    def kdeSvnPath( self ):
        return "branches/work/kdab-post-4.0/kdepim"

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
        return self.doPackaging( "kdepim", "20071219", True )
		
if __name__ == '__main__':
    subclass().execute()
