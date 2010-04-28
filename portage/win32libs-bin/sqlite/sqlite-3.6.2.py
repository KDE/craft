from Package.BinaryPackageBase import *
import os
import shutil
import utils
import info


PACKAGE_NAME         = "sqlite"
PACKAGE_DLL_NAME     = "sqlite3"
PACKAGE_VER_MAJOR    = "3"
PACKAGE_VER_MINOR    = "6"
PACKAGE_VER_RELEASE  = "2"
PACKAGE_VER          = "%s.%s.%s" % ( PACKAGE_VER_MAJOR, PACKAGE_VER_MINOR, PACKAGE_VER_RELEASE )
PACKAGE_FULL_VER     = PACKAGE_VER
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_FULL_NAME    = "%s_%s_%s" % ( PACKAGE_VER_MAJOR, PACKAGE_VER_MINOR, PACKAGE_VER_RELEASE )

SRC_URI= """
http://www.sqlite.org/sqlite-%s_%s_%s.zip
http://www.sqlite.org/sqlitedll-%s_%s_%s.zip
http://www.sqlite.org/sqlite-amalgamation-%s_%s_%s.zip
""" % ( PACKAGE_VER_MAJOR, PACKAGE_VER_MINOR, PACKAGE_VER_RELEASE, PACKAGE_VER_MAJOR, PACKAGE_VER_MINOR, PACKAGE_VER_RELEASE, PACKAGE_VER_MAJOR, PACKAGE_VER_MINOR, PACKAGE_VER_RELEASE )

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[PACKAGE_VER] = SRC_URI
        self.defaultTarget = PACKAGE_VER
        self.targetDigests[PACKAGE_VER] = ['78b3c8758ee4eb6cb4404283a1e754e7d35a6a87',
                                           '1464dfe5469c8ba108f2d55a19bfa049659eb120',
                                           '11e3419fab41ffc9c7213e211e301195f3519be0']        

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/sed'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True
    
class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        self.createCombinedPackage = True

    def install( self ):
        dst = os.path.join( self.imageDir(), "bin" )
        utils.cleanDirectory( dst )
        dst = os.path.join( self.imageDir(), "include" )
        utils.cleanDirectory( dst )
        dst = os.path.join( self.imageDir(), "lib" )
        utils.cleanDirectory( dst )
        dst = os.path.join( self.imageDir(), "src" )
        utils.cleanDirectory( dst )

        src = os.path.join( self.imageDir(), PACKAGE_DLL_NAME + ".dll" )
        dst = os.path.join( self.imageDir(), "bin", PACKAGE_DLL_NAME + ".dll" )
        utils.moveFile( src, dst )
        src = os.path.join( self.imageDir(), PACKAGE_DLL_NAME + ".exe" )
        dst = os.path.join( self.imageDir(), "bin", PACKAGE_DLL_NAME + ".exe" )
        utils.moveFile( src, dst )
        src = os.path.join( self.imageDir(), PACKAGE_DLL_NAME + ".h" )
        dst = os.path.join( self.imageDir(), "include", PACKAGE_DLL_NAME + ".h" )
        utils.moveFile( src, dst )
        src = os.path.join( self.imageDir(), PACKAGE_DLL_NAME + "ext.h" )
        dst = os.path.join( self.imageDir(), "include", PACKAGE_DLL_NAME + "ext.h" )
        utils.moveFile( src, dst )
        src = os.path.join( self.imageDir(), PACKAGE_DLL_NAME + ".def" )
        dst = os.path.join( self.imageDir(), "lib", PACKAGE_DLL_NAME + ".def" )
        utils.moveFile( src, dst )
        src = os.path.join( self.imageDir(), PACKAGE_DLL_NAME + ".c" )
        dst = os.path.join( self.imageDir(), "src", PACKAGE_DLL_NAME + ".c" )
        utils.moveFile( src, dst )
        utils.createImportLibs( PACKAGE_DLL_NAME, self.imageDir() )
        os.makedirs( os.path.join( self.installDir(), "lib" ,"pkgconfig" ))
        utils.copyFile( os.path.join( self.packageDir(), "sqlite3.pc" ), os.path.join( self.installDir(), "lib","pkgconfig", "sqlite3.pc" ) )
        return True

if __name__ == '__main__':
    Package().execute()
