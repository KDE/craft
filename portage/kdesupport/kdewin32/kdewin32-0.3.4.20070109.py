import os
import sys
import base

DEPEND = """
virtual/base
libs/qt
"""

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.instsrcdir = "kdewin32"

    def kdeSvnPath( self ):
        return "trunk/kdesupport/kdewin32"

    def unpack( self ):
        return self.kdeSvnUnpack()

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        if self.traditional:
            self.instdestdir = "kde"
            return self.doPackaging( "kdewin32", "0.3.4-1", True )
        else:
            return self.doPackaging( "kdewin32", os.path.basename(sys.argv[0]).replace("kdewin32-", "").replace(".py", ""), True )
if __name__ == '__main__':
    subclass().execute()
