import os
import utils
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['3.6.23.1'] = 'http://www.sqlite.org/sqlite-amalgamation-3.6.23.1.tar.gz'
        self.targets['3.7.2'] = 'http://www.sqlite.org/sqlite-amalgamation-3_7_2.zip'
        self.targets['3.7.15.2'] = 'http://www.sqlite.org/sqlite-amalgamation-3071502.zip'
        self.targets['3.8.0.1'] = 'https://www.sqlite.org/2013/sqlite-amalgamation-3080001.zip'
        self.targets['3.8.1.0'] = 'http://sqlite.org/2013/sqlite-amalgamation-3080100.zip'

        self.targetDigests['3.7.15.2'] = '1312016fdbb1dd6cb5a38bc05d1d051d9dc0e93e'
        self.targetDigests['3.7.2'] = 'e37304dffaf6e1b38357113ee9845cadff05e958'
        self.targetDigests['3.8.0.1'] = '73b2c4ae0cbbd630163f974cf1551bbacbfffa6f'
        self.targetDigests['3.8.1.0'] = '75a1ab154e796d2d1b391a2c7078679e15512bda'

        self.patchToApply['3.6.23.1'] = [("sqlite_cmake_and_wince_20100923.diff", 1)]
        self.patchToApply['3.7.2']    = [("sqlite_cmake_and_wince_20100923.diff", 1)]
        self.patchToApply['3.7.15.2'] = [("sqlite_cmake_and_wince_20130124.diff", 1)]
        self.patchToApply['3.8.0.1'] = [("sqlite_cmake_and_wince_20130124.diff", 1)]
        self.patchToApply['3.8.1.0'] = [("sqlite_cmake_and_wince_20130124.diff", 1)]
        
        self.targetInstSrc['3.6.23.1'] = "sqlite-3.6.23.1"
        self.targetInstSrc['3.7.15.2'] = "sqlite-amalgamation-3071502"
        self.targetInstSrc['3.8.0.1'] = "sqlite-amalgamation-3080001"
        self.targetInstSrc['3.8.1.0'] = "sqlite-amalgamation-3080100"
        
        self.shortDescription = "a library providing a self-contained, serverless, zero-configuration, transactional SQL database engine"
        self.defaultTarget = '3.8.1.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        if emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs/wcecompat'] = 'default'

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
