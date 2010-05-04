import os
import utils
import info
from Package.CMakePackageBase import *



class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.6.23.1'] = 'http://www.sqlite.org/sqlite-amalgamation-3.6.23.1.tar.gz'
        self.targetInstSrc['3.6.23.1'] = "sqlite-3.6.23.1"
        self.patchToApply['3.6.23.1'] = ( "sqlite-3.6.23.1-20100504.diff", 1 )
        self.defaultTarget = '3.6.23.1'
        
        
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        if platform.isCrossCompilingEnabled():
            self.hardDependencies['win32libs-sources/wcecompat-src'] = 'default'

class Package(CMakePackageBase):
  def __init__( self ):
    self.subinfo = subinfo()
    CMakePackageBase.__init__(self)
    
  def make(self, unused=''):
    if self.isTargetBuild():
        # Set the include path for the wcecompat files (e.g. errno.h). Setting it through
        # the Configure script generates errors due to the the backslashes in the path
        wcecompatincdir = os.path.join( os.path.join( self.mergeDestinationDir(), "include" ), "wcecompat" )
        os.environ["TARGET_INCLUDE"] = wcecompatincdir + ";" + os.getenv("TARGET_INCLUDE")
        
    return CMakePackageBase.make( self )


if __name__ == '__main__':
    Package().execute()
