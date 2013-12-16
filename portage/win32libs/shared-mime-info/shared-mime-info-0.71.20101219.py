import os
import utils
import info
import re
import shutil
import info
import compiler

from Package.CMakePackageBase import *
# do not forget to update CMakeLists.txt!
SRC_URI={'0.71': """
http://people.freedesktop.org/~hadess/shared-mime-info-0.71.tar.bz2
http://ftp.gnome.org/pub/gnome/sources/glib/2.24/glib-2.24.0.tar.bz2
""", '1.0': """
http://people.freedesktop.org/~hadess/shared-mime-info-1.0.tar.xz
http://ftp.gnome.org/pub/gnome/sources/glib/2.24/glib-2.24.0.tar.bz2
""", '1.1': """
http://people.freedesktop.org/~hadess/shared-mime-info-1.1.tar.xz
http://ftp.gnome.org/pub/gnome/sources/glib/2.24/glib-2.24.0.tar.bz2
"""}
GLIB_VER = "2.24.0"

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['0.71', '1.0','1.1']:
            self.targets[ ver ] = SRC_URI[ver]
            self.targetInstSrc[ ver ] = "shared-mime-info-" + ver
        self.targetDigests['0.71'] = ['6f3d3379662857646b0c5b95d5d26e47c0b6250a',
                                      '32714e64fff52d18db5f077732910215790e0c5b']
        self.targetDigests['1.0'] = ['146dbad62f5450116b0353f88bb8e700f0034013',
                                     '32714e64fff52d18db5f077732910215790e0c5b']
        self.targetDigests['1.1'] = ['752668b0cc5729433c99cbad00f21241ec4797ef',
                                     '32714e64fff52d18db5f077732910215790e0c5b']
        self.shortDescription = "common mimetype library"
        self.defaultTarget = '1.1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/gettext'] = 'default'
        self.dependencies['win32libs/libxml2'] = 'default'
        self.dependencies['gnuwin32/sed'] = 'default'

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
      directory = os.path.join( self.glibDir, "glib" )
      if ( os.path.exists( directory ) ):
          for root, dirs, files in os.walk( directory, topdown=False ):
              print(root)
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
        if compiler.isMinGW():
            manifest = os.path.join( self.packageDir(), "update-mime-database.exe.manifest" )
            executable = os.path.join( self.installDir(), "bin", "update-mime-database.exe" )
            utils.embedManifest( executable, manifest )
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
