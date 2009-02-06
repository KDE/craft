import base
import os
import sys
import shutil
import utils
import info


class subinfo(info.infoclass):
    def setTargets( self ):
      self.targets['1.9.2-2'] = 'http://downloads.sourceforge.net/sourceforge/gnuwin32/libiconv-1.9.2-1.exe'
      self.targetInstSrc['1.9.2-2'] = ''

      self.targets['1.12'] = 'http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.12.tar.gz'
      self.targetInstSrc['1.12'] = 'libiconv-1.12'
      self.patchToApply['1.12'] = ( 'iconv-src-1.12.patch', 0 )
      self.defaultTarget = '1.12'


class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
    self.subinfo = subinfo()

  def unpack( self ):

    if self.buildTarget == "1.9.2-2":
      # hopefully only one...
      for filename in self.filenames:
        os.system( os.path.join( self.downloaddir, filename ) + " /DIR=\"" + self.workdir + "\" /SILENT")
      return True

    return base.baseclass.unpack( self )

  def compile( self ):
    if self.buildTarget == "1.9.2-2":
      # binary-only package - nothing to compile
      return True
    return self.msysCompile()

  def install( self ):
    if self.buildTarget == "1.9.2-2":
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

    return self.msysInstall()

  def qmerge( self ):
    print >> sys.stderr, "Installing this package is not intented."
    return False

  def make_package( self ):
    # auto-create both import libs with the help of pexports
    for libs in "libiconv2 libcharset1".split():
        if not self.createImportLibs( libs ):
            return False;

    # now do packaging with kdewin-packager
    self.doPackaging( "libiconv", self.buildTarget, False )

    return True
  
if __name__ == '__main__':
    subclass().execute()
