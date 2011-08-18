# This package-script is automatically updated by the script win32libsupdater.py
# which can be found in your emerge/bin folder. To update this package, run
# win32libsupdater.py (and commit the results)
# based on revision git886de0cc9b787069382ac2e9c21bfdd0f31d215d

from Package.BinaryPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'

        for version in [ '1.47.0' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'boost-bjam', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'boost-bjam', version, '.tar.bz2.sha1' )

        self.defaultTarget = '1.47.0'


    def setDependencies( self ):
        self.dependencies['win32libs-bin/boost-headers'] = 'default'
        if not utils.envAsBool( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'gnuwin32/wget' ] = 'default'


    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
