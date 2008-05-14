import base
import os
import shutil
import utils
from utils import die

PACKAGE_NAME         = "libnova"
PACKAGE_VER          = "0.12.1"
PACKAGE_FULL_VER     = "0.12.1"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_FULL_VER )

SRC_URI= """
http://downloads.sourceforge.net/""" + PACKAGE_NAME + """/""" + PACKAGE_FULL_NAME + """.tar.gz
"""

DEPEND = """
kdesupport/kdewin32
"""

#
# this library is used by kdeedu/kstars
# the library is c-only 
#

class subclass(base.baseclass):
    def __init__( self, **args ):
        base.baseclass.__init__( self, SRC_URI, args=args )
        self.instsrcdir = PACKAGE_NAME
        self.createCombinedPackage = True

    def execute( self ):
        base.baseclass.execute( self )
        if self.compiler <> "mingw":
            print "error: can only be build with MinGW right now."
            exit( 1 )

    def unpack( self ):
        if( not base.baseclass.unpack( self ) ):
            return False
            
        src = os.path.join( self.workdir, self.instsrcdir )

        cmd = "cd %s && patch -p0 < %s" % \
              ( self.workdir, os.path.join( self.packagedir , "libnova.diff" ) )
        if utils.verbose() >= 1:
            print cmd
        os.system( cmd ) or die
        shutil.move( os.path.join( self.workdir, PACKAGE_FULL_NAME ), os.path.join( self.workdir, PACKAGE_NAME ) )
        return True

    def msysConfigureFlags ( self ):
        if self.traditional:
            kdewin_include_path = utils.toMSysPath( os.path.join( self.rootdir, "kde", "include" ) )
            kdewin_lib_path = utils.toMSysPath( os.path.join( self.rootdir, "kde", "lib" ) )
        else:
            kdewin_include_path = utils.toMSysPath( os.path.join( self.rootdir, "include" ) )
            kdewin_lib_path = utils.toMSysPath( os.path.join( self.rootdir, "lib" ) )
        
        flags = "--prefix=/ CFLAGS=-I" + kdewin_include_path + " LDFLAGS=-L" + kdewin_lib_path + "\\ -lkdewin32"
        return flags

    def compile( self ):
        return self.msysCompile( False )

    def install( self ):
        return self.msysInstall( False )

    def make_package( self ):
        dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
        utils.cleanDirectory( dst )

        self.stripLibs( "libnova" )
        self.createImportLibs( "libnova" )
        # now do packaging with kdewin-packager
        # it's a in-source build, do not pack sources
        self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, False )

        return True

if __name__ == '__main__':
    subclass().execute()
