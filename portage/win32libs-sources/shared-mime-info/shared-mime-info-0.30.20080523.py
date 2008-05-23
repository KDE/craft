import base
import os
import shutil
import utils
import info
import re

PACKAGE_NAME         = "shared-mime-info"
PACKAGE_VER          = "0.30"
PACKAGE_FULL_VER     = "0.30"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
GLIB_VER             = "2.14.5"

SRC_URI= """
http://people.freedesktop.org/~hadess/""" + PACKAGE_FULL_NAME + """.tar.bz2
ftp://ftp.gtk.org/pub/glib/2.14/glib-""" + GLIB_VER + """.tar.bz2
"""


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.30'] = SRC_URI
        self.targetInstSrc['0.30'] = PACKAGE_FULL_NAME
        self.defaultTarget = '0.30'

    def setDependencies( self ):
        self.hardDependencies['dev-util/win32libs'] = 'default'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
    self.subinfo = subinfo()

  def unpack( self ):
    if(not base.baseclass.unpack( self ) ):
      return False;
    
    # rename config.h and glibconfig.h.win32 in glib to 
    # avoid config.h confusion
    p = re.compile('.*\.[ch]$')
    glibdir = os.path.join( self.workdir, "glib-" + GLIB_VER )
    sedcmd = r"""-e "s/config.h/config.h.win32/" """
    dir = os.path.join( glibdir, "glib" )
    if ( os.path.exists( dir ) ):
        for root, dirs, files in os.walk( dir, topdown=False ):
            print root
            for name in files:
                if( p.match( name ) ):
                    utils.sedFile( root, name, sedcmd )

    # we have an own cmake script - copy it to the right place
    src = os.path.join( self.packagedir , "CMakeLists.txt" )
    dst = os.path.join( self.workdir, self.instsrcdir, "CMakeLists.txt" )
    shutil.copy( src, dst )

    src = os.path.join( self.packagedir , "config.h.cmake" )
    dst = os.path.join( self.workdir, self.instsrcdir, "config.h.cmake" )
    shutil.copy( src, dst )

    if( self.compiler == "mingw"):
        return True
    return self.kdeSvnUnpack( "trunk/kdesupport", "kdewin32")

  def kdeDefaultDefines( self ):
    # adjust some vars for proper compile
    cmake_src  = os.path.join( self.workdir, self.instsrcdir )

    options = "-DKDEWIN32_DIR=%s " % \
              os.path.join( self.workdir, "kdewin32" ).replace( "\\", "/" )

    options = options + "-DGLIB_DIR=%s " % \
              os.path.join( self.workdir, "glib-" + GLIB_VER ).replace( "\\", "/" )

    options = options + "-DCMAKE_INCLUDE_PATH=%s " % \
              os.path.join( self.rootdir, "win32libs", "include" ).replace( "\\", "/" )

    options = options + "-DCMAKE_LIBRARY_PATH=%s " % \
              os.path.join( self.rootdir, "win32libs", "lib" ).replace( "\\", "/" )

    self.kdeCustomDefines = "-DCMAKE_BUILD_TYPE=Release -DGLIB_DIR=%s" % \
              os.path.join( self.workdir, "glib-" + GLIB_VER ).replace( "\\", "/" )
    

    return options

  def compile( self ):
    self.kdeCustomDefines = self.kdeDefaultDefines()
    return self.kdeCompile()

  def install( self ):
    if( not self.kdeInstall() ):
        return False
    cmd = os.path.join( self.imagedir, self.instdestdir, "bin", "update-mime-database.exe" ) \
        + " " + os.path.join( self.imagedir, "share", "mime" )
    self.system( cmd )
    return True

  def make_package( self ):
    cmd = "strip -s %s" % \
          os.path.join(self.imagedir, self.instdestdir, "bin", "update-mime-database.exe" )
    self.system( cmd )

    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, self.buildTarget, True )

    return True
  
if __name__ == '__main__':
    subclass().execute()
