import base
import os
import shutil
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        ver = '1.2.40'
        self.targets[ver] = 'http://downloads.sourceforge.net/libpng/libpng-' + ver + '.tar.gz'
        self.targetInstSrc[ver] = 'libpng-' + ver
        self.defaultTarget = ver
    
    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/zlib'] = 'default'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
    self.buildType = "Release"
    self.subinfo = subinfo()

  def unpack( self ):
    if( not self.kdeSvnUnpack() ):
      return False
    # the cmake script is in libpng-src/scripts
    srcdir  = os.path.join( self.workdir, self.instsrcdir, "scripts", "CMakeLists.txt" )
    destdir = os.path.join( self.workdir, self.instsrcdir,            "CMakeLists.txt" )
    shutil.copy( srcdir, destdir )
    
    return True

  def compile( self ):
    self.kdeCustomDefines = "-DPNG_TESTS=OFF -DPNG_STATIC=OFF -DPNG_NO_STDIO=OFF"
    return self.kdeCompile()

  def install( self ):
    return self.kdeInstall()

  def make_package( self ):
    # auto-create both import libs with the help of pexports
    self.stripLibs( "libpng12" )

    # auto-create both import libs with the help of pexports
    self.createImportLibs( "libpng12" )

    # now do packaging with kdewin-packager
    self.doPackaging( "libpng", self.buildTarget )

    return True

if __name__ == '__main__':
    subclass().execute()
