import base
import os
import sys

DEPEND = """
kdesupport/taglib
kde/kdelibs
kde/kdebase
testing/ruby
testing/phonon
"""

class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "amarok"

    def kdeSvnPath( self ):
        return "trunk/extragear/multimedia/amarok"
        
    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        return self.doPackaging( "amarok", os.path.basename(sys.argv[0]).replace("amarok-", "").replace(".py", ""), True )

if __name__ == '__main__':		
    subclass().execute()
