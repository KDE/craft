import base
import os
import shutil
import re
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.18'] = "http://www.littlecms.com/lcms-1.18.tar.gz"
        self.targetInstSrc['1.18'] = "lcms-1.18"
        self.patchToApply['1.18'] = ( 'lcms-1.18.patch', 0 )
        self.defaultTarget = '1.18'

    def setDependencies( self ):
        self.hardDependencies['dev-util/msys'] = 'default'

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
      return False;
    # the .tar.gz ships a wrong icc34.h - it must be generated from icc34.h.in
    file = os.path.join( self.workdir, self.instsrcdir, "include", "icc34.h" )
    if( os.path.isfile( file ) ):
      os.remove( file )
    return True

  def compile( self ):
    return self.msysCompile()

  def install( self ):
    return self.msysInstall()

  def make_package( self ):
    # clean directory
    dst = os.path.join( self.imagedir, self.instdestdir, "lib" )
    utils.cleanDirectory( dst )

    self.stripLibs( "liblcms-1" )

    # auto-create both import libs with the help of pexports
    self.createImportLibs( "liblcms-1" )

    # now do packaging with kdewin-packager
    self.doPackaging( "lcms", self.buildTarget, True )

    return True

if __name__ == '__main__':
    subclass().execute()
