import base
import os
import utils
import info
import shutil

class subinfo(info.infoclass):
    def setTargets( self ):
        ver = '1.14'
        self.targets[ver]       = 'ftp://alpha.gnu.org/pub/gnu/libidn/libidn-%s.tar.gz' % ver
        self.targetInstSrc[ver] = 'libidn-%s' % ver
        self.defaultTarget = ver

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'


class subclass(base.baseclass):
  def __init__( self, **args ):
        base.baseclass.__init__( self, args=args )
        self.createCombinedPackage = True
        self.subinfo = subinfo()

  def execute( self ):
    base.baseclass.execute( self )
    if self.compiler <> "mingw":
      print "error: can only be build with MinGW (but in the end a \
             mingw/msvc combined package is created"
      exit( 1 )

  def unpack( self ):    
    if( not base.baseclass.unpack( self ) ):
      return False

    # we have an own cmake script - copy it to the right place
    src = os.path.join( self.packagedir , "CMakeLists.txt" )
    dst = os.path.join( self.workdir, self.instsrcdir, "CMakeLists.txt" )
    shutil.copy( src, dst )

    src = os.path.join( self.packagedir , "config.h.cmake" )
    dst = os.path.join( self.workdir, self.instsrcdir, "config.h.cmake" )
    shutil.copy( src, dst )

    src = os.path.join( self.packagedir , "idn-int.h.cmake" )
    dst = os.path.join( self.workdir, self.instsrcdir, "idn-int.h.cmake" )
    shutil.copy( src, dst )

    return True

  def compile( self ):
      return self.kdeCompile()

  def install( self ):
      return self.kdeInstall()

  def make_package( self ):
    # clean directory
    dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
    utils.cleanDirectory( dst )

    self.stripLibs( "libidn-11" )
    self.createImportLibs( "libidn-11" )

    # now do packaging with kdewin-packager
    self.doPackaging( "libidn", self.buildTarget, True )

    return True

if __name__ == '__main__':
    subclass().execute()
