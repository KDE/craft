import base
import os
import shutil
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        ver = '7.19.4'
        self.targets[ver] = 'http://curl.haxx.se/download/curl-' + ver + '.tar.bz2'
        self.targetInstSrc[ver] = 'curl-' + ver
        self.defaultTarget = ver

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.buildType = "Release"
    self.subinfo = subinfo()

  def unpack( self ):
    if( not base.baseclass.unpack( self ) ):
      return False
    # we have an own cmake script - copy it to the right place
    cmake_script = os.path.join( self.packagedir , "CMakeLists.txt" )
    cmake_dest = os.path.join( self.workdir, self.instsrcdir, "CMakeLists.txt" )
    shutil.copy( cmake_script, cmake_dest )

    return True

  def compile( self ):
    return self.kdeCompile()

  def install( self ):
    return self.kdeInstall()

  def make_package( self ):
    self.doPackaging( "libcurl", self.buildTarget, True )
    return True

if __name__ == '__main__':
    subclass().execute()
