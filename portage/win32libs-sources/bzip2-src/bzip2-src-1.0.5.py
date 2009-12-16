import base
import os
import shutil
import utils
import info

PACKAGE_NAME         = "libbzip2"

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.0.4-6'] = 'http://www.bzip.org/1.0.4/bzip2-1.0.4.tar.gz'
        self.targetInstSrc['1.0.4-6'] = "bzip2-1.0.4"
        self.targets['1.0.5-1'] = 'http://www.bzip.org/1.0.5/bzip2-1.0.5.tar.gz'
        self.targetInstSrc['1.0.5-1'] = "bzip2-1.0.5"
        self.defaultTarget = '1.0.5-1'

class subclass(base.baseclass):
  def __init__( self, **args ):
    base.baseclass.__init__( self, args=args )
    self.createCombinedPackage = True
    self.buildType = "Release"
    self.subinfo = subinfo()

  def unpack( self ):
    if( not base.baseclass.unpack( self ) ):
      return False
    # we have an own cmake script - copy it to the right place
    cmake_script = os.path.join( self.packagedir , "CMakeLists.txt" )
    cmake_dest = os.path.join( self.workdir, self.instsrcdir, "CMakeLists.txt" )
    shutil.copy( cmake_script, cmake_dest )

    bzip2_dir  = os.path.join( self.workdir, self.instsrcdir )

    cmd = "cd %s && patch -p0 < %s" % \
          ( bzip2_dir, os.path.join( self.packagedir, "bzip.diff" ) )
    utils.system( cmd )

    return True

  def compile( self ):
    return self.kdeCompile()

  def install( self ):
    return self.kdeInstall()

  def make_package( self ):
    # do packaging with kdewin-packager
    self.doPackaging( PACKAGE_NAME, self.buildTarget, True )

    return True

if __name__ == '__main__':
    subclass().execute()
