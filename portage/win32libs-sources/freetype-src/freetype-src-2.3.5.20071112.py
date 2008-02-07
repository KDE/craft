import base
import os
import utils
import shutil
import info

PACKAGE_NAME         = "freetype"
PACKAGE_VER          = "2.3.5"
PACKAGE_FULL_VER     = "2.3.5-1"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "libfreetype-6"


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.3.5-1'] = "http://download.savannah.gnu.org/releases/" + PACKAGE_NAME + "/" + PACKAGE_FULL_NAME + ".tar.gz"
        self.targetInstSrc['2.3.5-1'] = PACKAGE_FULL_NAME
        self.defaultTarget = '2.3.5-1'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/kdewin32'] = 'default'
    
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.createCombinedPackage = True
        self.subinfo = subinfo()

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
        cmd = "cd %s && patch -p0 < %s" % \
              ( self.workdir, os.path.join( self.packagedir, "freetype.diff" ) )
        utils.system( cmd ) or utils.die( "patch" )
        return True

    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

        return True

if __name__ == '__main__':
    subclass().execute()
