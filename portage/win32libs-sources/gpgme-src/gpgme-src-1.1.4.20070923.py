import base
import os
import shutil
import re
import utils
from utils import die

PACKAGE_NAME         = "gpgme"
PACKAGE_VER          = "1.1.4"
PACKAGE_FULL_VER     = "1.1.4-3"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER)
PACKAGE_GPGERR_NAME  = "%s-%s" % ( "libgpg-error", "1.5")
PACKAGE_DLL_NAME     = """
libgpg-error-0
libgpgme-11
"""

SRC_URI= """
ftp://ftp.gnupg.org/gcrypt/gpgme/""" + PACKAGE_FULL_NAME + """.tar.bz2
ftp://ftp.gnupg.org/gcrypt/libgpg-error/""" + PACKAGE_GPGERR_NAME + """.tar.bz2
"""

DEPEND = """
"""

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, SRC_URI, args=args )
    self.instsrcdir = PACKAGE_FULL_NAME
    self.createCombinedPackage = True

  def execute( self ):
    base.baseclass.execute( self )
    if self.compiler <> "mingw":
      print "error: can only be build with MinGW (but in the end a \
             mingw/msvc combined package is created"
      exit( 1 )

  def unpack( self ):
    if( not base.baseclass.unpack( self ) ):
      return False
    src = os.path.join( self.workdir )
    gpgerr_dir = os.path.join( src, PACKAGE_GPGERR_NAME )
    gpgme_dir  = os.path.join( src, PACKAGE_FULL_NAME )

    cmd = "cd %s && patch -p0 < %s" % \
          ( gpgerr_dir, os.path.join( self.packagedir, "libgpg-error-1.5.diff" ) )
    os.system( cmd ) or die

    cmd = "cd %s && patch -p0 < %s" % \
          ( gpgme_dir, os.path.join( self.packagedir, "gpgme-1.1.4.diff" ) )
    os.system( cmd ) or die

    return True

  def msysConfigureFlags ( self ):
    flags  = base.baseclass.msysConfigureFlags( self )
    flags += "--with-gpg-error-prefix=%s" % \
             utils.toMSysPath( os.path.join( self.imagedir, self.instdestdir ) )
    return flags

  def compile( self ):
    self.instsrcdir = PACKAGE_GPGERR_NAME
    if( not self.msysCompile() ):
        return False
    if( not self.msysInstall() ):
        return False

    self.instsrcdir = PACKAGE_FULL_NAME
    gpgerr_inst_dir = os.path.join( self.imagedir, self.instdestdir )
    os.environ[ "LDFLAGS" ] = "-L" + utils.toMSysPath( os.path.join( gpgerr_inst_dir, "lib" ) )
    os.environ[ "CFLAGS" ]  = "-I" + utils.toMSysPath( os.path.join( gpgerr_inst_dir, "include" ) )
    return self.msysCompile()

  def install( self ):
    self.instsrcdir = PACKAGE_GPGERR_NAME
    if( not self.msysInstall() ):
        return False

    self.instsrcdir = PACKAGE_FULL_NAME
    return self.msysInstall()

  def make_package( self ):
    # clean directory
    dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
    utils.cleanDirectory( dst )

    for lib in PACKAGE_DLL_NAME.split():
        self.stripLibs( lib )

    # auto-create both import libs with the help of pexports
    for lib in PACKAGE_DLL_NAME.split():
        self.createImportLibs( lib )

    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

    return True

if __name__ == '__main__':
    subclass().execute()
