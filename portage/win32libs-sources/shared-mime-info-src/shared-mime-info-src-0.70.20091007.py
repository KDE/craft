import base
import os
import shutil
import utils
import info
import re

# do not forget to update CMakeLists.txt!
SRC_URI= """
http://people.freedesktop.org/~hadess/shared-mime-info-0.70.tar.bz2
ftp://ftp.gtk.org/pub/glib/2.18/glib-2.18.3.tar.bz2
"""
GLIB_VER = "2.18.3"

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.70'] = SRC_URI
        self.targetInstSrc['0.70'] = "shared-mime-info-0.70"
        self.defaultTarget = '0.70'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['win32libs-bin/gettext'] = 'default'
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
    self.subinfo = subinfo()

  def unpack( self ):
    if(not base.baseclass.unpack( self ) ):
      return False;
    if not self.kde.kdeSvnUnpack( "trunk/kdesupport", "kdewin"):
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
    src = os.path.join( self.packagedir , "FindLibintl.cmake" )
    dst = os.path.join( self.workdir, self.instsrcdir, "FindLibintl.cmake" )
    shutil.copy( src, dst )

    src = os.path.join( self.packagedir , "config.h.cmake" )
    dst = os.path.join( self.workdir, self.instsrcdir, "config.h.cmake" )
    shutil.copy( src, dst )

    return True

  def kdeDefaultDefines( self ):
    # adjust some vars for proper compile
    cmake_src  = os.path.join( self.workdir, self.instsrcdir )

    options = "-DKDEWIN32_DIR=%s " % \
              os.path.join( self.workdir, "kdewin" ).replace( "\\", "/" )

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
    self.doPackaging( "shared-mime-info", self.buildTarget, True )

    return True
  
if __name__ == '__main__':
    subclass().execute()
