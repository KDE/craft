import os
import utils
import info
from Package.CMakePackageBase import *



class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.6.23.1'] = 'http://www.sqlite.org/sqlite-amalgamation-3.6.23.1.tar.gz'
        self.targetInstSrc['3.6.23.1'] = "sqlite-3.6.23.1"
        self.defaultTarget = '3.6.23.1'

class Package(CMakePackageBase):
  def __init__( self ):
    self.subinfo = subinfo()
    CMakePackageBase.__init__(self)


  def unpack( self ):
    if( not CMakePackageBase.unpack( self ) ):
      return False
    # copy CMakeLists.txt
    utils.copyFile( os.path.join( self.packageDir(), "CMakeLists.txt" ),
                    os.path.join( self.sourceDir(),  "CMakeLists.txt" ) )
    return True


    return CMakePackageBase.createPackage( self )

if __name__ == '__main__':
    Package().execute()
