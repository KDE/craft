import base
import os
import shutil
import utils
import info

PACKAGE_NAME         = "libxslt"
PACKAGE_VER          = "1.1.23+"
PACKAGE_FULL_VER     = "1.1.23-2"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER)
PACKAGE_DLL_NAMES    = """
libxslt
libexslt
"""
PACKAGE_INSTSRCDIR   = PACKAGE_FULL_NAME + ".win32"

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[PACKAGE_VER] = "ftp://ftp.zlatkovic.com/pub/libxml/" + PACKAGE_FULL_NAME + ".win32.zip"
        self.targetInstSrc[PACKAGE_VER] = PACKAGE_FULL_NAME
        self.defaultTarget = PACKAGE_VER

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
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
    # a small patch is needed
    cmd = "cd %s && patch -p0 < %s" % \
          ( os.path.join( self.workdir, self.instsrcdir ), \
            os.path.join( self.packagedir, "libxslt_mingw.patch" ) )
    self.system( cmd ) or utils.die( "patch" )

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
    for libs in PACKAGE_DLL_NAMES.split():
        shutil.copy( os.path.join( src, libs + ".lib" ), os.path.join( dst, libs + ".lib" ) )
    
    return True
  def make_package( self ):
    self.instsrcdir = PACKAGE_INSTSRCDIR

    # auto-create both import libs with the help of pexports
    for libs in PACKAGE_DLL_NAMES.split():
        self.createImportLibs( libs )

    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, False )

    return True

if __name__ == '__main__':
    subclass().execute()
