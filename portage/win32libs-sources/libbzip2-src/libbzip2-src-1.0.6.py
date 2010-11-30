import utils
import info
from Package.CMakePackageBase import *

##########################################################################
############################# ATTENTION ##################################
##########################################################################
######### There is no binary build for Windows Ce, just the lib! #########
##########################################################################

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.0.6-1'] = 'http://www.bzip.org/1.0.6/bzip2-1.0.6.tar.gz'
        self.targetInstSrc['1.0.6-1'] = "bzip2-1.0.6"
        self.patchToApply['1.0.6-1'] = ("bzip.diff", 1)
        self.targetDigests['1.0.6-1'] = '3f89f861209ce81a6bab1fd1998c0ef311712002'
        self.shortDescription = "shared libraries for handling bzip2 archives (runtime)"
        self.defaultTarget = '1.0.6-1'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        if emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs-sources/wcecompat-src'] = 'default'

class Package(CMakePackageBase):
  def __init__( self ):
    self.subinfo = subinfo()
    CMakePackageBase.__init__(self)
    self.subinfo.options.package.packageName = 'libbzip2'

  def createPackage( self ):
    # auto-create both import libs with the help of pexports
    self.createImportLibs( "bzip2" )

    return CMakePackageBase.createPackage( self )

if __name__ == '__main__':
    Package().execute()
