import base
import os
import shutil
import utils
from utils import die

PACKAGE_NAME         = "jasper"
PACKAGE_VER          = "1.900.1"
PACKAGE_FULL_VER     = "1.900.1-2"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "libjasper"

SRC_URI= """
http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-1.900.1.zip
"""

# fixme: we only need jpeg as dependency!
DEPEND = """
dev-util/win32libs
"""

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, SRC_URI, args=args )
    self.instsrcdir = os.path.join( PACKAGE_FULL_NAME, "src", "libjasper" )
    self.createCombinedPackage = True
    self.buildType = "Release"

  def unpack( self ):
    if( not base.baseclass.unpack( self ) ):
      return False
    # we have an own cmake script - copy it to the right place
    cmake_script = os.path.join( self.packagedir , "CMakeLists.txt" )
    cmake_dest = os.path.join( self.workdir, self.instsrcdir, "CMakeLists.txt" )
    shutil.copy( cmake_script, cmake_dest )

    return True

  def kdeDefaultDefines( self ):
    # adjust some vars for proper compile
    cmake_src  = os.path.join( self.workdir, self.instsrcdir )

    options = "%s -DCMAKE_INSTALL_PREFIX=%s " % \
              ( cmake_src, self.rootdir.replace( '\\', '/' ) )
    options = options + "-DCMAKE_INCLUDE_PATH=%s " % \
              os.path.join( self.rootdir, "win32libs", "include" ).replace( "\\", "/" )

    options = options + "-DCMAKE_LIBRARY_PATH=%s " % \
              os.path.join( self.rootdir, "win32libs", "lib" ).replace( "\\", "/" )

    return options

  def compile( self ):
    return self.kdeCompile()

  def install( self ):
    return self.kdeInstall()

  def make_package( self ):
    # auto-create both import libs with the help of pexports
    self.stripLibs( PACKAGE_DLL_NAME )

    # auto-create both import libs with the help of pexports
    self.createImportLibs( PACKAGE_DLL_NAME )

    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, True )

    return True
  
if __name__ == '__main__':
    subclass().execute()
