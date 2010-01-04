import base
import os
import sys
import shutil
import utils
import info


class subinfo(info.infoclass):
    def setTargets( self ):
      for ver in ( '1.12', '1.13', '1.13.1' ):
        self.targets[ver]       = 'http://ftp.gnu.org/pub/gnu/libiconv/libiconv-%s.tar.gz' % ver
        self.targetInstSrc[ver] = 'libiconv-%s' % ver
        self.patchToApply[ver]  = ( 'iconv-src-%s.patch' % ver, 0 )
      self.defaultTarget = '1.13.1'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/msys'] = 'default'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
    self.subinfo = subinfo()

  def compile( self ):
    return self.msysCompile()

  def install( self ):
    return self.msysInstall()

  def qmerge( self ):
    print >> sys.stderr, "Installing this package is not intented."
    return False

  def make_package( self ):
    # libxml2.dll is linked against iconv.dll ... :(
    in_lib  = os.path.join( self.imagedir, "bin", "libiconv-2.dll" )
    out_lib = os.path.join( self.imagedir, "bin", "iconv.dll" )
    if os.path.exists( in_lib ):
      shutil.copy( in_lib, out_lib )

    # auto-create both import libs with the help of pexports
    for libs in "libiconv-2 libcharset-1".split():
        if not self.createImportLibs( libs ):
            return False;

    # now do packaging with kdewin-packager
    self.doPackaging( "iconv", self.buildTarget )

    return True
  
if __name__ == '__main__':
    subclass().execute()
