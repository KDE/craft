import os
import sys
import base
import info
import utils
import shutil

class subinfo(info.infoclass):

    def setTargets( self ):
        if os.getenv("KDECOMPILER") == "mingw":
            self.targets['4.1'] = "http://www.cs.nyu.edu/exact/core/gmp/gmp-static-mingw-4.1.tar.gz"
        else:
            self.targets['4.1'] = "http://www.cs.nyu.edu/exact/core/gmp/gmp-static-vc-4.1.2.zip"
        self.defaultTarget = '4.1'

class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.subinfo = subinfo()

    def unpack( self ):
        base.baseclass.unpack( self )
        return True

    def install( self ):
        if os.getenv("KDECOMPILER") == "mingw":
            utils.copySrcDirToDestDir( os.path.join(self.workdir, "gmp"), self.imagedir )
        else:
            dst = os.path.join( self.imagedir, "include" )
            utils.cleanDirectory( dst )
            dst = os.path.join( self.imagedir, "lib" )
            utils.cleanDirectory( dst )

            src = os.path.join( self.workdir, "gmp-static", "gmp.lib" )
            dst = os.path.join( self.imagedir, "lib", "gmp.lib" )
            shutil.copy( src, dst )
            src = os.path.join( self.workdir, "gmp-static", "gmpDebug.lib" )
            dst = os.path.join( self.imagedir, "lib", "gmpDebug.lib" )
            shutil.copy( src, dst )
            src = os.path.join( self.workdir, "gmp-static", "gmp.h" )
            dst = os.path.join( self.imagedir, "include", "gmp.h" )
            shutil.copy( src, dst )
        
        return True

if __name__ == '__main__':
    subclass().execute()
