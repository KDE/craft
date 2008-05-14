import base
import os
import shutil
import utils

# attn: you need http://innounp.sourceforge.net/ !!

PACKAGE_NAME         = "openssl"
PACKAGE_VER          = "0.9.8g"
PACKAGE_FULL_VER     = "0.9.8g-1"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DL_NAME      = "Win32OpenSSL-0_9_8g.exe"
PACKAGE_DLL_NAMES     = """
libeay32
ssleay32
"""

SRC_URI= """
http://www.slproweb.com/download/""" + PACKAGE_DL_NAME + """
"""

DEPEND = """
"""

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, SRC_URI, args=args )
    self.createCombinedPackage = True

  def unpack( self ):
    # make sure that the workdir is empty
    utils.cleanDirectory( self.workdir )

    cmd = os.path.join( self.downloaddir, PACKAGE_DL_NAME )
    cmd = "innounp.exe -x " + cmd + " -d" + os.path.join( self.workdir )
    os.system( cmd ) and utils.die( cmd )

    return True

  def compile( self ):
    # binary-only package - nothing to compile
    return True

  def install( self ):
    # cleanup
    dst = os.path.join( self.imagedir, self.instdestdir )
    utils.cleanDirectory( dst )

    dst = os.path.join( self.imagedir, self.instdestdir, "bin" )
    utils.cleanDirectory( dst )

    # bin
    for libs in PACKAGE_DLL_NAMES.split():
        src = os.path.join( self.workdir, self.instsrcdir, "{sys}", libs + ".dll" )
        dst = os.path.join( self.imagedir, self.instdestdir, "bin", libs + ".dll" )
        shutil.copy( src, dst )
    # lib
    dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
    src = os.path.join( self.workdir, self.instsrcdir, "{app}", "lib", "VC" )
    utils.copySrcDirToDestDir( src, dst )
    # copy two mingw files separate
    src = os.path.join( self.workdir, self.instsrcdir, "{app}", "lib", "MinGW" )
    shutil.copy( os.path.join( src, "libeay32.a" ), os.path.join( dst, "libeay32.a" ) )
    shutil.copy( os.path.join( src, "libeay32.a" ), os.path.join( dst, "libeay32d.a" ) )
    shutil.copy( os.path.join( src, "ssleay32.a" ), os.path.join( dst, "libssleay32.a" ) )
    shutil.copy( os.path.join( src, "ssleay32.a" ), os.path.join( dst, "libssleay32d.a" ) )

    dst = os.path.join( dst, "static" )
    utils.cleanDirectory( dst )
    os.removedirs( dst )

    # include
    src = os.path.join( self.workdir, self.instsrcdir, "{app}", "include" )
    dst = os.path.join( self.imagedir, self.instdestdir, "include" )
    utils.copySrcDirToDestDir( src, dst )


    return True
  def make_package( self ):

    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, False )

    return True
  
if __name__ == '__main__':
    subclass().execute()
