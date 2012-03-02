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

        for version in [ '0.9.1', '0.9.2', '0.9.5' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'libofx', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'libofx', version, '.tar.bz2.sha1' )

        self.shortDescription = '''a parser and an API for the OFX (Open Financial eXchange) specification'''

        self.defaultTarget = '0.9.5'


    def setDependencies( self ):
        if not utils.envAsBool( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'virtual/bin-base' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/libopensp' ] = 'default'
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
