# This package-script is automatically updated by the script win32libsupdater.py
# which can be found in your emerge/bin folder. To update this package, run
# win32libsupdater.py (and commit the results)
# based on revision git300e71be83450407a947422dca7250fbfcbbea49

from Package.BinaryPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'

        for version in [ '1.47.0', '1.44.0', '1.48.0' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'boost-thread', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'boost-thread', version, '.tar.bz2.sha1' )

        self.shortDescription = '''portable C++ libraries'''

        self.defaultTarget = '1.48.0'


    def setDependencies( self ):
        if not utils.envAsBool( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'virtual/bin-base' ] = 'default'


    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
