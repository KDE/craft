# This package-script is automatically updated by the script win32libsupdater.py
# which can be found in your emerge/bin folder. To update this package, run
# win32libsupdater.py (and commit the results)
# based on revision git517fe8408cfc04c16e44590384bd78d065060149

from Package.BinaryPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'

        for version in [ '0.60.6-3', '0.60.5-1', '0.60.6', '0.60.6.1-3' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'aspell', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'aspell', version, '.tar.bz2.sha1' )

        self.shortDescription = '''A powerful spell checker, designed to replace ispell'''

        self.defaultTarget = '0.60.6.1-3'


    def setDependencies( self ):
        if not utils.envAsBool( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'virtual/bin-base' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/win_iconv' ] = 'default'


    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
