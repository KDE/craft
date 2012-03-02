# This package-script is automatically updated by the script win32libsupdater.py
# which can be found in your emerge/bin folder. To update this package, run
# win32libsupdater.py (and commit the results)
# based on revision gite7334d6def1c6f20056c837da2331bea4304d765

from Package.BinaryPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'

        for version in [ '0.4.7-1', '0.5.0-1', '20091008', '20090812', '0.4.4', '0.4.7', '0.4.6', '0.5.2-1' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'libssh', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'libssh', version, '.tar.bz2.sha1' )

        self.shortDescription = '''a working SSH implementation by the mean of a library'''

        self.defaultTarget = '0.5.2-1'


    def setDependencies( self ):
        if not utils.envAsBool( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'virtual/bin-base' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/zlib' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/openssl' ] = 'default'


    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
