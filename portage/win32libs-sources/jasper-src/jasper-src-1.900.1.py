import base
import os
import shutil
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '1.900.1-2' ] = 'http://www.ece.uvic.ca/~mdadams/jasper/software/jasper-1.900.1.zip'
        self.targetInstSrc[ '1.900.1-2' ] = os.path.join( 'jasper-1.900.1', 'src', 'libjasper' )
        self.defaultTarget = '1.900.1-2'

    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/jpeg'] = 'default'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
    self.subinfo = subinfo()

  def unpack( self ):
    if( not base.baseclass.unpack( self ) ):
      return False
    # we have an own cmake script - copy it to the right place
    cmake_script = os.path.join( self.packagedir , "CMakeLists.txt" )
    cmake_dest = os.path.join( self.workdir, self.instsrcdir, "CMakeLists.txt" )
    shutil.copy( cmake_script, cmake_dest )

    return True

  def compile( self ):
    return self.kdeCompile()

  def install( self ):
    return self.kdeInstall()

  def make_package( self ):
    # auto-create both import libs with the help of pexports
    self.stripLibs( "libjasper" )

    # auto-create both import libs with the help of pexports
    self.createImportLibs( "libjasper" )

    # now do packaging with kdewin-packager
    self.doPackaging( "jasper", self.buildTarget, True )

    return True

if __name__ == '__main__':
    subclass().execute()
