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

SRC_URI= """
http://download.savannah.gnu.org/releases/""" + PACKAGE_NAME + """/""" + PACKAGE_FULL_NAME + """.tar.gz
"""

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['2.3.5-1'] = SRC_URI
        self.defaultTarget = '2.3.5-1'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/kdewin32'] = 'default'
    
class subclass(base.baseclass):
    def __init__(self):
        base.baseclass.__init__( self, SRC_URI )
        self.instsrcdir = PACKAGE_FULL_NAME
        self.createCombinedPackage = True
        self.subinfo = subinfo()

    def execute( self ):
        base.baseclass.execute( self )
        if self.compiler <> "mingw":
            print "error: can only be build with MinGW right now."
            exit( 1 )

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
        return True

    def msysConfigureFlags ( self ):
        flags = "CPPFLAGS=-I/d/cygopt/kde-root/include LDFLAGS=-L/d/cygopt/kde-root/lib --prefix=/ "
        return flags

    def compile( self ):
        return self.msysCompile( False )

    def install( self ):
        if not self.msysInstall( False ):
            return False
        src = os.path.join( self.imagedir, self.instdestdir, "bin", PACKAGE_DLL_NAME + ".dll" )
        dst = os.path.join( self.imagedir, self.instdestdir, "bin", "lib" + PACKAGE_NAME + ".dll" )
        shutil.copyfile( src, dst )
        if os.path.exists( os.path.join( self.imagedir, self.instdestdir, "bin", PACKAGE_NAME + "-config" ) ):
            os.remove(os.path.join( self.imagedir, self.instdestdir, "bin", PACKAGE_NAME + "-config" ) )
        return True

    def make_package( self ):
        dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
        utils.cleanDirectory( dst )
        src = os.path.join( self.imagedir, self.instdestdir, "bin", PACKAGE_DLL_NAME + ".dll" )
        dst = os.path.join( self.imagedir, self.instdestdir, "bin", "lib" + PACKAGE_NAME + ".dll" )
        shutil.copyfile( src, dst )
        if os.path.exists( os.path.join( self.imagedir, self.instdestdir, "bin", PACKAGE_NAME + "-config" ) ):
            os.remove( os.path.join( self.imagedir, self.instdestdir, "bin", PACKAGE_NAME + "-config" ) )

        #self.stripLibs( PACKAGE_DLL_NAME )
        #self.createImportLibs( "lib" + PACKAGE_NAME )
        # now do packaging with kdewin-packager
        # it's a in-source build, do not pack sources
        self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, False )

        return True

if __name__ == '__main__':
    subclass().execute()
