import base
import os
import utils
import info
import re
import shutil
import info
from Package.CMakePackageBase import *
# do not forget to update CMakeLists.txt!
SRC_URI= """
http://people.freedesktop.org/~hadess/shared-mime-info-0.71.tar.bz2
ftp://ftp.gtk.org/pub/glib/2.18/glib-2.18.3.tar.bz2
"""
GLIB_VER = "2.18.3"

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.71'] = SRC_URI
        self.targetInstSrc['0.71'] = "shared-mime-info-0.71"
        self.defaultTarget = '0.71'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['win32libs-bin/gettext'] = 'default'
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        # adjust some vars for proper compile
        self.glibDir=os.path.join( self.buildDir() , ".."  , "glib-" + GLIB_VER );
        self.subinfo.options.configure.defines = " -DGLIB_DIR=%s " % self.glibDir.replace( "\\", "/" )

           
    def unpack( self ):
      if(not CMakePackageBase.unpack( self ) ):
         return False;
      # rename config.h and glibconfig.h.win32 in glib to 
      # avoid config.h confusion
      p = re.compile('.*\.[ch]$')
      sedcmd = r"""-e "s/config.h/config.h.win32/" """
      dir = os.path.join( self.glibDir, "glib" )
      if ( os.path.exists( dir ) ):
          for root, dirs, files in os.walk( dir, topdown=False ):
              print root
              for name in files:
                  if( p.match( name ) ):
                      utils.sedFile( root, name, sedcmd )

      # we have an own cmake script - copy it to the right place
      src = os.path.join( self.packageDir() , "CMakeLists.txt" )
      dst = os.path.join( self.sourceDir() , "CMakeLists.txt" )
      shutil.copy( src, dst )
      src = os.path.join( self.packageDir() , "FindLibintl.cmake" )
      dst = os.path.join( self.sourceDir(), "FindLibintl.cmake" )
      shutil.copy( src, dst )
      
      src = os.path.join( self.packageDir() , "FindKDEWin.cmake" )
      dst = os.path.join( self.sourceDir(), "FindKDEWin.cmake" )
      shutil.copy( src, dst )
      
      
      src = os.path.join( self.packageDir() , "FindIconv.cmake" )
      dst = os.path.join( self.sourceDir(), "FindIconv.cmake" )
      shutil.copy( src, dst )

      src = os.path.join( self.packageDir() , "config.h.cmake" )
      dst = os.path.join( self.sourceDir(), "config.h.cmake" )
      shutil.copy( src, dst )

      return True

  
if __name__ == '__main__':
    Package().execute()