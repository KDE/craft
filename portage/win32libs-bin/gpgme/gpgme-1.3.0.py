# This package-script is automatically updated by the script win32libsupdater.py
# which can be found in your emerge/bin folder. To update this package, run
# win32libsupdater.py (and commit the results)
# based on revision 1

from Package.BinaryPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'

        for version in [ '1.1.4-3', '1.3.0' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'gpgme', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'gpgme', version , '.tar.bz2.sha1' )

        self.defaultTarget = '1.3.0'


    def setDependencies( self ):
        if not os.getenv( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'gnuwin32/wget' ] = 'default'
        self.runtimeDependencies[ 'win32libs-sources/assuan2-src' ] = 'default'
        self.runtimeDependencies[ 'win32libs-sources/gpg-error-src' ] = 'default'
        self.runtimeDependencies[ 'virtual/base' ] = 'default'


    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
