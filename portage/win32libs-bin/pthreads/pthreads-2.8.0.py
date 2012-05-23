# This package-script is automatically updated by the script win32libsupdater.py
# which can be found in your emerge/bin folder. To update this package, run
# win32libsupdater.py (and commit the results)
# based on revision gitcfc5b700df8db112d62408e5402ba6ed7170a64d

from Package.BinaryPackageBase import *
from Package.VirtualPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'

        for version in [ '2.8.0' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'pthreads', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'pthreads', version, '.tar.bz2.sha1' )

        self.defaultTarget = '2.8.0'


    def setDependencies( self ):
        if not utils.envAsBool( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'gnuwin32/wget' ] = 'default'


    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class PthreadsPackage(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if compiler.isMSVC() or compiler.getMinGWVersion() == "4.4.7":
    class Package(PthreadsPackage):
        def __init__( self ):
            PthreadsPackage.__init__( self )
else:
    class Package(VirtualPackageBase):
        def __init__( self ):
            self.subinfo = subinfo()
            VirtualPackageBase.__init__( self )

if __name__ == '__main__':
      Package().execute()
