import utils
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.0.5-1'] = 'http://www.bzip.org/1.0.5/bzip2-1.0.5.tar.gz'
        self.targetInstSrc['1.0.5-1'] = "bzip2-1.0.5"
        self.patchToApply['1.0.5-1'] = ("bzip.diff", 0)
        self.defaultTarget = '1.0.5-1'

class Package(CMakePackageBase):
  def __init__( self ):
    self.subinfo = subinfo()
    CMakePackageBase.__init__(self)
    self.subinfo.options.package.packageName = 'libbzip2'
    self.subinfo.options.package.withCompiler = None

  def buildType( self ):
    return "Release"

  def unpack( self ):
    if( not CMakePackageBase.unpack( self ) ):
      return False
    # copy CMakeLists.txt
    utils.copyFile( os.path.join( self.packageDir(), "CMakeLists.txt" ),
                    os.path.join( self.sourceDir(),  "CMakeLists.txt" ) )
    return True

  def createPackage( self ):
    # auto-create both import libs with the help of pexports
    self.createImportLibs( "libbzip2" )

    return CMakePackageBase.createPackage( self )

if __name__ == '__main__':
    Package().execute()
