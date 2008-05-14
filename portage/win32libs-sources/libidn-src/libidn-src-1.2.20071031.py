import base
import os
import utils

PACKAGE_NAME         = "libidn"
PACKAGE_VER          = "1.2"
PACKAGE_FULL_VER     = "1.2-1"
PACKAGE_FULL_NAME    = "%s-%s" % (PACKAGE_NAME, PACKAGE_VER)
PACKAGE_DLL_NAME     = """
libidn-11
"""

SRC_URI= """
ftp://alpha.gnu.org/pub/gnu/libidn/""" + PACKAGE_FULL_NAME + """.tar.gz
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

  def compile( self ):
    return self.msysCompile()

  def install( self ):
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
