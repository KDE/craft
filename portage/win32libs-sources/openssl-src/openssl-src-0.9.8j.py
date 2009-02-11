import base
import os
import shutil
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.9.8j'] = 'http://www.openssl.org/source/openssl-0.9.8j.tar.gz'
        self.targetInstSrc['0.9.8j'] = 'openssl-0.9.8j'
        self.defaultTarget = '0.9.8j'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
    self.subinfo = subinfo()

  def compile( self ):
    os.chdir( os.path.join( self.workdir, self.instsrcdir ) )
    cmd = "ms\mingw32.bat"
    return self.system( cmd )

  def install( self ):
    src = os.path.join( self.workdir, self.instsrcdir )
    dst = self.imagedir

    if not os.path.isdir( dst ):
      os.mkdir( dst )
    os.mkdir( os.path.join( dst, "bin" ) )
    os.mkdir( os.path.join( dst, "lib" ) )
    os.mkdir( os.path.join( dst, "include" ) )

    shutil.copy( os.path.join( src, "libeay32.dll" ) , os.path.join( dst, "bin" ) )
    shutil.copy( os.path.join( src, "libssl32.dll" ) , os.path.join( dst, "bin", "ssleay32.dll" ) )
    utils.copySrcDirToDestDir( os.path.join( src, "outinc" ) , os.path.join( dst, "include" ) )

    # auto-create both import libs with the help of pexports
    for f in "libeay32 ssleay32".split():
      self.stripLibs( f )
      self.createImportLibs( f )

    return True

  def make_package( self ):
    return self.doPackaging( "openssl", self.buildTarget + "-1", False )
  
if __name__ == '__main__':
    subclass().execute()
