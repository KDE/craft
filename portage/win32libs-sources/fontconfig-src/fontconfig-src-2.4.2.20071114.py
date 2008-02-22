import base
import os
import utils
import shutil
import info

PACKAGE_NAME         = "fontconfig"
PACKAGE_VER          = "2.4.2"
PACKAGE_FULL_VER     = "2.4.2-2"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "libfontconfig"

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.4.2-2'] = "http://fontconfig.org/release/" + PACKAGE_FULL_NAME + ".tar.gz"
        self.targetInstSrc['2.4.2-2'] = PACKAGE_FULL_NAME
        self.defaultTarget = '2.4.2-2'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/kdewin32'] = 'default'
        self.hardDependencies['win32libs-sources/freetype-src'] = 'default'
    
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, "" )
        self.createCombinedPackage = False
        self.subinfo = subinfo()

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
        cmd = "cd %s && patch -p0 < %s" % \
              ( self.workdir, os.path.join( self.packagedir, "fontconfig-cmake.diff" ) )
        self.system( cmd ) or utils.die( "patch" )

        return True

    def kdeSvnPath( self ):
        return False
    
    def compile( self ):
        return self.kdeCompile()

    def install( self ):
        return self.kdeInstall()

    def make_package( self ):
        self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

        return True

if __name__ == '__main__':
    subclass().execute()
