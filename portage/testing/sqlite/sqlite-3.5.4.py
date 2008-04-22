import base
import os
import shutil
import re
import utils
from utils import die
import info

PACKAGE_NAME         = "sqlite"
PACKAGE_DLL_NAME     = "sqlite3"
PACKAGE_VER          = "3.5.4"
PACKAGE_FULL_VER     = "3.5.4"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )

SRC_URI= """
http://www.sqlite.org/sqlite-3_5_4.zip
http://www.sqlite.org/sqlitedll-3_5_4.zip
http://www.sqlite.org/sqlite-amalgamation-3_5_4.zip
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.5.4'] = SRC_URI
        self.defaultTarget = '3.5.4'
    
class subclass(base.baseclass):
    def __init__( self ):
        base.baseclass.__init__( self, SRC_URI )
        self.subinfo = subinfo()
    
    def unpack( self ):
        base.baseclass.unpack( self )
        return True
        
    def install( self ):
        dst = os.path.join( self.imagedir, "bin" )
        utils.cleanDirectory( dst )
        dst = os.path.join( self.imagedir, "include" )
        utils.cleanDirectory( dst )
        dst = os.path.join( self.imagedir, "lib" )
        utils.cleanDirectory( dst )

        src = os.path.join( self.workdir, PACKAGE_DLL_NAME + ".dll" )
        dst = os.path.join( self.imagedir, "bin", PACKAGE_DLL_NAME + ".dll" )
        shutil.copy( src, dst )
        src = os.path.join( self.workdir, PACKAGE_DLL_NAME + ".exe" )
        dst = os.path.join( self.imagedir, "bin", PACKAGE_DLL_NAME + ".exe" )
        shutil.copy( src, dst )
        src = os.path.join( self.workdir, PACKAGE_DLL_NAME + ".h" )
        dst = os.path.join( self.imagedir, "include", PACKAGE_DLL_NAME + ".h" )
        shutil.copy( src, dst )
        src = os.path.join( self.workdir, PACKAGE_DLL_NAME + "ext.h" )
        dst = os.path.join( self.imagedir, "include", PACKAGE_DLL_NAME + "ext.h" )
        shutil.copy( src, dst )
        src = os.path.join( self.workdir, PACKAGE_DLL_NAME + ".def" )
        dst = os.path.join( self.imagedir, "lib", PACKAGE_DLL_NAME + ".def" )
        shutil.copy( src, dst )
        self.createImportLibs( PACKAGE_DLL_NAME )
        return True
    
if __name__ == '__main__':
    subclass().execute()
