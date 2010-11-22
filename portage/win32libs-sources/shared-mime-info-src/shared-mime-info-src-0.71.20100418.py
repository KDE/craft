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
http://ftp.gnome.org/pub/gnome/sources/glib/2.24/glib-2.24.0.tar.bz2
"""
GLIB_VER = "2.24.0"

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.71'] = SRC_URI
        self.targetInstSrc['0.71'] = "shared-mime-info-0.71"
        self.targetDigests['0.71'] = ['6f3d3379662857646b0c5b95d5d26e47c0b6250a',
                                      '32714e64fff52d18db5f077732910215790e0c5b']
        self.defaultTarget = '0.71'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/gettext'] = 'default'
        self.dependencies['win32libs-bin/libxml2'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

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

      src = os.path.join( self.packageDir() , "CheckMingwVersion.cmake" )
      dst = os.path.join( self.sourceDir(), "CheckMingwVersion.cmake" )
      shutil.copy( src, dst )

      src = os.path.join( self.packageDir() , "config.h.cmake" )
      dst = os.path.join( self.sourceDir(), "config.h.cmake" )
      shutil.copy( src, dst )

      src = os.path.join( self.packageDir() , "dirent.c" )
      dst = os.path.join( self.sourceDir(), "dirent.c" )
      shutil.copy( src, dst )

      src = os.path.join( self.packageDir() , "unistd.c" )
      dst = os.path.join( self.sourceDir(), "unistd.c" )
      shutil.copy( src, dst )

      if not os.path.exists( os.path.join( self.sourceDir(), "headers" ) ):
        os.makedirs( os.path.join( self.sourceDir(), "headers" ) )

      src = os.path.join( self.packageDir(), "dirent.h" )
      dst = os.path.join( self.sourceDir(), "headers", "dirent.h" )
      shutil.copy( src, dst )

      src = os.path.join( self.packageDir() , "unistd.h" )
      dst = os.path.join( self.sourceDir(), "headers", "unistd.h" )
      shutil.copy( src, dst )

      utils.applyPatch( self.glibDir , os.path.join( self.packageDir(), "glib-x64.diff" ), 0 )

      return True

    def install( self ):
        if not CMakePackageBase.install( self ): 
            return False
        manifest = os.path.join( self.packageDir(), "update-mime-database.exe.manifest" )
        patch = os.path.join( self.installDir(), "bin", "update-mime-database.exe" )
        cmd = "mt.exe -nologo -manifest %s -outputresource:%s;1" % ( manifest, patch )
        utils.system( cmd )

        return True

    def qmerge( self ):
        # When crosscompiling also install into the targets directory
        ret = CMakePackageBase.qmerge(self)
        if emergePlatform.isCrossCompilingEnabled():
            target_mimedir = os.path.join(ROOTDIR, emergePlatform.targetPlatform(),
                            "share", "mime", "packages")
            build_mime = os.path.join(self.imageDir(), "share", "mime",
                         "packages", "freedesktop.org.xml")
            utils.createDir(target_mimedir)
            if not os.path.exists(build_mime):
                utils.error("Could not find mime file: %s" % build_mime)
                return False
            utils.copyFile(build_mime, target_mimedir)
        return ret


if __name__ == '__main__':
    Package().execute()
