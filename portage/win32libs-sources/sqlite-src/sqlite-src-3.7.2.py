import os
import utils
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.6.23.1'] = 'http://www.sqlite.org/sqlite-amalgamation-3.6.23.1.tar.gz'
        self.targets['3.7.2'] = 'http://www.sqlite.org/sqlite-amalgamation-3_7_2.zip'
        self.targetDigests['3.7.2'] = "e37304dffaf6e1b38357113ee9845cadff05e958"
        self.patchToApply['3.7.2']    = ("sqlite_cmake_and_wince_20100923.diff", 1)
        self.patchToApply['3.6.23.1'] = ("sqlite_cmake_and_wince_20100923.diff", 1)
        self.targetInstSrc['3.6.23.1'] = "sqlite-3.6.23.1"
        self.defaultTarget = '3.7.2'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        if emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs-sources/wcecompat-src'] = 'default'

class Package(CMakePackageBase):
  def __init__( self ):
    self.subinfo = subinfo()
    CMakePackageBase.__init__(self)
    if emergePlatform.isCrossCompilingEnabled() and self.isTargetBuild():
        self.subinfo.options.configure.defines = "-DSTATIC_LIBRARY=ON"

  def make(self, unused=''):
    if self.isTargetBuild():
        # Set the include path for the wcecompat files (e.g. errno.h). Setting it through
        # the Configure script generates errors due to the the backslashes in the path
        wcecompatincdir = os.path.join( os.path.join( self.mergeDestinationDir(), "include" ), "wcecompat" )
        os.environ["TARGET_INCLUDE"] = wcecompatincdir + ";" + os.getenv("TARGET_INCLUDE")

    return CMakePackageBase.make( self )

if __name__ == '__main__':
    Package().execute()
