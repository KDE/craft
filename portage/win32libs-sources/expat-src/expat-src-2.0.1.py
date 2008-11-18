import base
import os
import sys
import shutil
import utils
import info

PACKAGE_DLL_NAME     = "libexpat"

class subinfo(info.infoclass):
    def setTargets( self ):
      self.targets['2.0.1'] = 'http://downloads.sourceforge.net/sourceforge/expat/expat-win32bin-2.0.1.exe'
      self.targetInstSrc['2.0.1'] = ''
      self.defaultTarget = '2.0.1'


class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
    self.subinfo = subinfo()

  def unpack( self ):

    # hopefully only one...
    for filename in self.filenames:
        self.system( os.path.join( self.downloaddir, filename ) + " /DIR=\"" + self.workdir + "\" /SILENT")

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

    src = os.path.join( self.workdir, self.instsrcdir, "bin", PACKAGE_DLL_NAME + ".dll" )
    dst = os.path.join( self.imagedir, self.instdestdir, "bin", PACKAGE_DLL_NAME + ".dll" )
    shutil.copy( src, dst )

    # /contrib/expat/self.buildTarget
    dst = os.path.join( self.imagedir, self.instdestdir, "contrib" )
    utils.cleanDirectory( dst )
    dst = os.path.join( dst, "expat" )
    utils.cleanDirectory( dst )
    dst = os.path.join( dst, self.buildTarget )
    utils.cleanDirectory( dst )

    src = os.path.join( self.workdir )
    shutil.copy( os.path.join( src, "README.txt" ),  os.path.join( dst, "README.txt" ) )

    # /doc can be used from zip package
    src = os.path.join( self.workdir, self.instsrcdir, "doc" )
    dst = os.path.join( self.imagedir, self.instdestdir, "doc" )
    utils.copySrcDirToDestDir( src, dst )

    # /include needs a rebuild... :(
    src = os.path.join( self.workdir, self.instsrcdir, "Source", "lib" )
    dst = os.path.join( self.imagedir, self.instdestdir, "include" )
    utils.cleanDirectory( dst )
    shutil.copy( os.path.join( src, "expat.h" ),  os.path.join( dst, "expat.h" ) )
    shutil.copy( os.path.join( src, "expat_external.h" ),  os.path.join( dst, "expat_external.h" ) )

    # /lib needs a complete rebuild - done in make_package
    dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
    utils.cleanDirectory( dst )

    return True

  def qmerge( self ):
    print >> sys.stderr, "Installing this package is not intented."
    return False

  def make_package( self ):
    # auto-create both import libs with the help of pexports
    self.createImportLibs( PACKAGE_DLL_NAME )

    # now do packaging with kdewin-packager
    self.doPackaging( "expat", self.buildTarget, True )

    return True
  
if __name__ == '__main__':
    subclass().execute()
