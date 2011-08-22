# This package-script is automatically updated by the script win32libsupdater.py
# which can be found in your emerge/bin folder. To update this package, run
# win32libsupdater.py (and commit the results)
# based on revision git0c46359075d9f0529d17ced5d1bc304fa9a04201

from Package.BinaryPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'

        for version in [ '3.10', '3.20', '3.14', '3.20-1' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'cfitsio', version, packagetypes=['lib'] )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'cfitsio', version, '.tar.bz2.sha1', packagetypes=['lib'] )

        self.defaultTarget = '3.20-1'


    def setDependencies( self ):
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
