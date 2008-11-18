import base
import os
import sys
import shutil
import utils
import info

PACKAGE_NAME         = "libiconv"
PACKAGE_DLL_NAMES    = """
libiconv2
libcharset1
"""

class subinfo(info.infoclass):
    def setTargets( self ):
      self.targets['1.9.2-2'] = 'http://heanet.dl.sourceforge.net/sourceforge/gnuwin32/libiconv-1.9.2-1.exe'
      self.targetInstSrc['1.9.2-2'] = ''
      self.defaultTarget = '1.9.2-2'


class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
    self.subinfo = subinfo()

  def unpack( self ):

    # hopefully only one...
    for filename in self.filenames:
        os.system( os.path.join( self.downloaddir, filename ) + " /DIR=\"" + self.workdir + "\" /SILENT")

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

    # /contrib/libiconv/self.buildTarget
    src = os.path.join( self.workdir, self.instsrcdir, "contrib" )
    dst = os.path.join( self.imagedir, self.instdestdir, "contrib" )
    utils.copySrcDirToDestDir( src, dst )

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
    for libs in PACKAGE_DLL_NAMES.split():
        if not self.createImportLibs( libs ):
            return False;

    # now do packaging with kdewin-packager
    self.doPackaging( "libiconv", self.buildTarget, False )

    return True
  
if __name__ == '__main__':
    subclass().execute()
