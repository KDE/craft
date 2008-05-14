import base
import os
import shutil
import utils

PACKAGE_NAME         = "aspell"
PACKAGE_VER          = "0.50.3"
PACKAGE_FULL_VER     = "0.50.3-4"
PACKAGE_FULL_NAME    = "%s-%s" % ( PACKAGE_NAME, PACKAGE_VER )
PACKAGE_DLL_NAMES     = """
aspell-15
pspell-15
"""
PACKAGE_CONTRIB_FILES= """
COPYING
README
"""

SRC_URI= """
http://ftp.gnu.org/gnu/aspell/w32/aspell-dev-0-50-3-3.zip
http://ftp.gnu.org/gnu/aspell/w32/Aspell-0-50-3-3-Setup.exe
"""

DEPEND = """
"""

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, SRC_URI, args=args )
    self.createCombinedPackage = False

  def unpack( self ):
    # make sure that the workdir is empty
    utils.cleanDirectory( self.workdir )

    # hopefully only one...
    for filename in self.filenames:
        ( shortname, ext ) = os.path.splitext( filename )
        if( ext == ".exe" ):
            os.system( os.path.join( self.downloaddir, filename ) + " /DIR=\"" + self.workdir + "\" /VERYSILENT")
        else:
            if( not utils.unpackFile( self.downloaddir, filename, self.workdir ) ):
                return False

    return True

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

    for libs in PACKAGE_DLL_NAMES.split():
        src = os.path.join( self.workdir, self.instsrcdir, "bin", libs + ".dll" )
        dst = os.path.join( self.imagedir, self.instdestdir, "bin", libs + ".dll" )
        shutil.copy( src, dst )

    # /contrib/PACKAGE_NAME/PACKAGE_FULL_VER
    dst = os.path.join( self.imagedir, self.instdestdir, "contrib" )
    utils.cleanDirectory( dst )
    dst = os.path.join( dst, PACKAGE_NAME )
    utils.cleanDirectory( dst )
    dst = os.path.join( dst, PACKAGE_FULL_VER )
    utils.cleanDirectory( dst )

    src = os.path.join( self.workdir )
    for f in PACKAGE_CONTRIB_FILES.split():
        shutil.copy( os.path.join( src, f ),  os.path.join( dst, f ) )

    # /doc can be used from zip package
    src = os.path.join( self.workdir, self.instsrcdir, "doc" )
    dst = os.path.join( self.imagedir, self.instdestdir, "doc" )
    utils.copySrcDirToDestDir( src, dst )

    # /data can be used from zip package
    src = os.path.join( self.workdir, self.instsrcdir, "data" )
    dst = os.path.join( self.imagedir, self.instdestdir, "data" )
    utils.copySrcDirToDestDir( src, dst )

    # /include comes from devel package
    src = os.path.join( self.workdir, self.instsrcdir, "aspell-dev-0-50-3-3", "include" )
    dst = os.path.join( self.imagedir, self.instdestdir, "include" )
    utils.copySrcDirToDestDir( src, dst )

    # /lib needs a complete rebuild - done in make_package
    dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
    utils.cleanDirectory( dst )

    return True
  def make_package( self ):
    self.instsrcdir = ""

    # auto-create both import libs with the help of pexports
    # one problem here - aspell has also a c++ interface which can't be used...
    for libs in PACKAGE_DLL_NAMES.split():
        self.createImportLibs( libs )

    # now do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, PACKAGE_FULL_VER, False )

    return True
  
if __name__ == '__main__':
    subclass().execute()
