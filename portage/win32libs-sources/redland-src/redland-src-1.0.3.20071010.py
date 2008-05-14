import base
import os
import shutil
import utils

PACKAGE_NAME         = "redland"
PACKAGE_VER          = "1.0.3"
PACKAGE_FULL_VER     = "1.0.3-5"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAMES    = """
libcurl
libdb43
librdf
raptor
rasqal
"""
PACKAGE_CONTRIB_FILES= """
AUTHORS
COPYING
COPYING.LIB
LICENSE.txt
LICENSE-2.0.txt
NOTICE
README
"""

SRC_URI= """
http://download.librdf.org/binaries/win32/1.0.3/redland-1.0.3-Win32-Dev.zip
"""

DEPEND = """
"""

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, SRC_URI, args=args )
    self.createCombinedPackage = True

  def compile( self ):
    # binary-only package - nothing to compile
    return True

  def install( self ):
    # cleanup
    dst = os.path.join( self.imagedir )
    utils.cleanDirectory( dst )
    dst = os.path.join( self.imagedir, self.instdestdir )
    utils.cleanDirectory( dst )

    # /bin only contains zlib1.dll
    dst = os.path.join( self.imagedir, self.instdestdir, "bin" )
    utils.cleanDirectory( dst )

    for libs in PACKAGE_DLL_NAMES.split():
        src = os.path.join( self.workdir, self.instsrcdir, libs + ".dll" )
        dst = os.path.join( self.imagedir, self.instdestdir, "bin", libs + ".dll" )
        shutil.copy( src, dst )

    # /contrib/PACKAGE_NAME/PACKAGE_FULL_VER
    dst = os.path.join( self.imagedir, self.instdestdir, "contrib" )
    utils.cleanDirectory( dst )
    dst = os.path.join( dst, PACKAGE_NAME )
    utils.cleanDirectory( dst )
    dst = os.path.join( dst, PACKAGE_FULL_VER )
    utils.cleanDirectory( dst )

    src = os.path.join( self.workdir )
    for f in PACKAGE_CONTRIB_FILES.split():
        shutil.copy( os.path.join( src, f ),  os.path.join( dst, f ) )

    # /include can be used from zip package
    src = os.path.join( self.workdir, self.instsrcdir, "include" )
    dst = os.path.join( self.imagedir, self.instdestdir, "include", "redland" )
    utils.copySrcDirToDestDir( src, dst )

    # /lib needs a complete rebuild - done in make_package
    dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
    utils.cleanDirectory( dst )

    return True
  def make_package( self ):
    self.instsrcdir = ""

    # auto-create both import libs with the help of pexports
    for libs in PACKAGE_DLL_NAMES.split():
        self.createImportLibs( libs )

    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, False )

    return True
  
if __name__ == '__main__':
    subclass().execute()
