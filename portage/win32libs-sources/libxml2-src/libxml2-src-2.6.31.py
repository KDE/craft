import base
import os
import shutil
import utils
import info

PACKAGE_NAME         = "libxml2"
PACKAGE_VER          = "2.6.31"
PACKAGE_FULL_VER     = "2.6.31-1"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAME     = "libxml2"
PACKAGE_INSTSRCDIR   = PACKAGE_FULL_NAME + ".win32"

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.6.31-1'] = "ftp://ftp.zlatkovic.com/pub/libxml/" + PACKAGE_FULL_NAME + ".win32.zip"
        self.targetInstSrc['2.6.31-1'] = PACKAGE_FULL_NAME
        self.defaultTarget = '2.6.31-1'
    def setDependencies( self ):
        return

class subclass(base.baseclass):
  def __init__(self):
    base.baseclass.__init__( self, "" )
    self.createCombinedPackage = True
    self.subinfo = subinfo()

  def compile( self ):
    # binary-only package - nothing to compile
    return True

  def install( self ):
    self.instsrcdir = PACKAGE_INSTSRCDIR
    # cleanup
    dst = os.path.join( self.imagedir )
    utils.cleanDirectory( dst )
    dst = os.path.join( self.imagedir, self.instdestdir )
    utils.cleanDirectory( dst )

    # /bin can be used from zip package
    src = os.path.join( self.workdir, self.instsrcdir, "bin" )
    dst = os.path.join( self.imagedir, self.instdestdir, "bin" )
    utils.copySrcDirToDestDir( src, dst )

    # /include can be used from zip package
    src = os.path.join( self.workdir, self.instsrcdir, "include" )
    dst = os.path.join( self.imagedir, self.instdestdir, "include" )
    utils.copySrcDirToDestDir( src, dst )

    # /contrib contains readme.txt
    dst = os.path.join( self.imagedir, self.instdestdir, "contrib" )
    utils.cleanDirectory( dst )
    dst = os.path.join( dst, PACKAGE_NAME )
    utils.cleanDirectory( dst )
    dst = os.path.join( dst, PACKAGE_FULL_VER )
    utils.cleanDirectory( dst )

    src = os.path.join( self.workdir, self.instsrcdir )
    shutil.copy( os.path.join( src, "readme.txt" ), os.path.join( dst, "readme.txt" ) )

    # /lib needs a complete rebuild - done in make_package
    src = os.path.join( self.workdir, self.instsrcdir, "lib" )
    dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
    utils.cleanDirectory( dst )
    # no need to recreate msvc import lib
    shutil.copy( os.path.join( src, PACKAGE_DLL_NAME + ".lib" ), os.path.join( dst, PACKAGE_DLL_NAME + ".lib" ) )
    
    return True
  def make_package( self ):
    self.instsrcdir = PACKAGE_INSTSRCDIR

    # auto-create both import libs with the help of pexports
    self.createImportLibs( PACKAGE_DLL_NAME )

    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, False )

    return True

if __name__ == '__main__':
    subclass().execute()
