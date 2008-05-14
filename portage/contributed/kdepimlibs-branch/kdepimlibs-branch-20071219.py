import base
import os
import utils

DEPEND = """
kde/kdelibs
"""

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.instsrcdir = "kdepimlibs"

    def kdeSvnPath( self ):
        return "branches/work/kdab-post-4.0/kdepimlibs"

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
        return self.doPackaging( "kdepimlibs", "20071219", True )
		
if __name__ == '__main__':
    subclass().execute()
