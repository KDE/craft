# -*- coding: utf-8 -*-
import base
import os
import shutil
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        ver = '4.999.9beta'
        self.targets[ver] = 'http://tukaani.org/xz/xz-4.999.9beta.tar.gz'
        self.targetInstSrc[ver] = 'xz-' + ver
        self.defaultTarget = ver
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'


class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.buildType = "Release"
    self.subinfo = subinfo()

  def execute( self ):
    base.baseclass.execute( self )
    if self.compiler != "mingw" and self.compiler != "mingw4":
      print "error: can only be build with MinGW (but in the end a \
             mingw/msvc combined package is created"
      exit( 1 )

  def unpack( self ):
    if( not base.baseclass.unpack( self ) ):
      return False
    # we have an own cmake script - copy it to the right place
    cmake_script = os.path.join( self.packagedir , "CMakeLists.txt" )
    cmake_dest = os.path.join( self.workdir, self.instsrcdir, "CMakeLists.txt" )
    shutil.copy( cmake_script, cmake_dest )

    cmake_script = os.path.join( self.packagedir , "config.h.cmake" )
    cmake_dest = os.path.join( self.workdir, self.instsrcdir, "config.h.cmake" )
    shutil.copy( cmake_script, cmake_dest )

    return True

  def compile( self ):
    return self.kdeCompile()

  def install( self ):
    return self.kdeInstall()

  def make_package( self ):
    self.createImportLibs( "liblzma" )
    self.doPackaging( "liblzma", self.buildTarget, True )
    return True

if __name__ == '__main__':
    subclass().execute()
