import base
import os
import shutil
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['7.19.3'] = 'http://curl.haxx.se/download/curl-7.19.3.tar.bz2'
        self.targetInstSrc['7.19.3'] = "curl-7.19.3"
        self.defaultTarget = '7.19.3'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
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
    # throw away possible debug symbols
    self.stripLibs( "libcurl" )

    # auto-create both import libs with the help of pexports
    self.createImportLibs( "libcurl" )

    # now do packaging with kdewin-packager
    self.doPackaging( "libcurl", self.buildTarget, True )

    return True

if __name__ == '__main__':
    subclass().execute()
