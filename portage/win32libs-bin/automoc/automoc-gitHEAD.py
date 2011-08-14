# This package-script is automatically updated by the script win32libsupdater.py
# which can be found in your emerge/bin folder. To update this package, run
# win32libsupdater.py (and commit the results)
# based on revision gitcde784c62d8d33d1d0882b77dc9c3f0da699415b

from Package.BinaryPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'

        for version in [ 'gitHEAD' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'automoc', version, packagetypes=['bin'] )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'automoc', version, '.tar.bz2.sha1', packagetypes=['bin'] )

        self.defaultTarget = 'gitHEAD'


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
