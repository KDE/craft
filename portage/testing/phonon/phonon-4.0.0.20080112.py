import base
import os
import sys

DEPEND = """
kde/kdelibs
"""

class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "phonon"

    def kdeSvnPath( self ):
        return "trunk/kdereview"
        
    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "phonon", os.path.basename(sys.argv[0]).replace("phonon-", "").replace(".py", ""), True )

if __name__ == '__main__':		
    subclass().execute()
