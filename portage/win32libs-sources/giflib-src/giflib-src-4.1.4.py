import base
import os
import sys
import shutil
import utils
import info

PACKAGE_DLL_NAME     = "giflib4"

class subinfo(info.infoclass):
    def setTargets( self ):
      self.targets['4.1.4-1'] = 'http://switch.dl.sourceforge.net/sourceforge/gnuwin32/giflib-4.1.4-1.exe'
      self.targetInstSrc['4.1.4-1'] = ''
      self.defaultTarget = '4.1.4-1'


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

    src = os.path.join( self.workdir, self.instsrcdir, "bin", PACKAGE_DLL_NAME + ".dll" )
    dst = os.path.join( self.imagedir, self.instdestdir, "bin", PACKAGE_DLL_NAME + "giflib4.dll" )
    shutil.copy( src, dst )

    # /contrib/giflib/self.buildTarget
    src = os.path.join( self.workdir, self.instsrcdir, "contrib" )
    dst = os.path.join( self.imagedir, self.instdestdir, "contrib" )
    utils.copySrcDirToDestDir( src, dst )

    # /doc can be used from zip package
    src = os.path.join( self.workdir, self.instsrcdir, "doc" )
    dst = os.path.join( self.imagedir, self.instdestdir, "doc" )
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
    if not self.createImportLibs( PACKAGE_DLL_NAME ):
        return False

    # now do packaging with kdewin-packager
    self.doPackaging( "giflib", self.buildTarget, False )

    return True
  
if __name__ == '__main__':
    subclass().execute()
