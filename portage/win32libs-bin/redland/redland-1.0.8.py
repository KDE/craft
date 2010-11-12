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

        for version in [ '1.0.8', '1.0.8-1', '1.0.8-2' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'redland', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'redland', version , '.tar.bz2.sha1' )

        self.defaultTarget = '1.0.8'


    def setDependencies( self ):
        if not os.getenv( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'gnuwin32/wget' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/sqlite' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/libcurl' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/libxslt' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/pcre' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/openssl' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/libxml2' ] = 'default'


    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
