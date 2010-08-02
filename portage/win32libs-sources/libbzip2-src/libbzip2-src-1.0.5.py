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
        self.targets['1.0.5-1'] = 'http://www.bzip.org/1.0.5/bzip2-1.0.5.tar.gz'
        self.targetInstSrc['1.0.5-1'] = "bzip2-1.0.5"
        self.patchToApply['1.0.5-1'] = ("bzip.diff", 1)
        self.targetDigests['1.0.5-1'] = '8b02713ea0c8eb501cc8bdac4432d7f29700f767'
        self.defaultTarget = '1.0.5-1'

    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
  def __init__( self ):
    self.subinfo = subinfo()
    CMakePackageBase.__init__(self)
    self.subinfo.options.package.packageName = 'libbzip2'
    self.subinfo.options.package.withCompiler = None

  def createPackage( self ):
    # auto-create both import libs with the help of pexports
    self.createImportLibs( "bzip2" )

    return CMakePackageBase.createPackage( self )

if __name__ == '__main__':
    Package().execute()
