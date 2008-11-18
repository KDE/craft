import base
import os
import sys
import shutil
import utils
import info

PACKAGE_NAME         = "zlib"
PACKAGE_FULL_VER     = "1.2.3-2"
PACKAGE_DLL_NAME     = "zlib1"

class subinfo(info.infoclass):
    def setTargets( self ):
      self.targets['1.2.3-2'] = 'http://www.zlib.net/zlib123-dll.zip'
      self.targetInstSrc['1.2.3-2'] = ''
      self.defaultTarget = '1.2.3-2'


class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
    self.subinfo = subinfo()

  def compile( self ):
    # binary-only package - nothing to compile
    return True

  def install( self ):
    # cleanup
    dst = os.path.join( self.imagedir )
    utils.cleanDirectory( dst )
    dst = os.path.join( self.imagedir, self.instdestdir )
    utils.cleanDirectory( dst )

    # /bin only contains zlib1.dll
    dst = os.path.join( self.imagedir, self.instdestdir, "bin" )
    utils.cleanDirectory( dst )

    src = os.path.join( self.workdir, self.instsrcdir, PACKAGE_DLL_NAME + ".dll" )
    dst = os.path.join( self.imagedir, self.instdestdir, "bin", PACKAGE_DLL_NAME + ".dll" )
    shutil.copy( src, dst )

    # /contrib/PACKAGE_NAME/PACKAGE_FULL_VER
    dst = os.path.join( self.imagedir, self.instdestdir, "contrib" )
    utils.cleanDirectory( dst )
    dst = os.path.join( dst, PACKAGE_NAME )
    utils.cleanDirectory( dst )
    dst = os.path.join( dst, PACKAGE_FULL_VER )
    utils.cleanDirectory( dst )

    src = os.path.join( self.workdir )
    shutil.copy( os.path.join( src, "DLL_FAQ.txt" ), os.path.join( dst, "DLL_FAQ.txt" ) )
    shutil.copy( os.path.join( src, "README.txt" ),  os.path.join( dst, "README.txt" ) )
    shutil.copy( os.path.join( src, "USAGE.txt" ),   os.path.join( dst, "USAGE.txt" ) )

    # /include can be used from zip package
    src = os.path.join( self.workdir, self.instsrcdir, "include" )
    dst = os.path.join( self.imagedir, self.instdestdir, "include" )
    utils.copySrcDirToDestDir( src, dst )

    # /lib needs a complete rebuild - done in make_package
    dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
    utils.cleanDirectory( dst )

    return True

  def qmerge( self ):
    print >> sys.stderr, "Installing this package is not intented."
    return False

  def make_package( self ):
    # auto-create both import libs with the help of pexports
    if not self.createImportLibs( PACKAGE_DLL_NAME ):
        return False

    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, self.buildTarget, False )

    return True
  
if __name__ == '__main__':
    subclass().execute()
