# This package-script is automatically updated by the script win32libsupdater.py
# which can be found in your emerge/bin folder. To update this package, run
# win32libsupdater.py (and commit the results)
# based on revision git2307c0b44f07114f16134d0d5f4db2e94b481eb4

from Package.BinaryPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'

        for version in [ '8.02', '8.12', '7.9', '7.8', '8.10', '8.21' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'pcre', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'pcre', version, '.tar.bz2.sha1' )

        self.shortDescription = '''Perl-Compatible Regular Expressions'''

        self.defaultTarget = '8.21'


    def setDependencies( self ):
        if not utils.envAsBool( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'virtual/bin-base' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/zlib' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/libbzip2' ] = 'default'


    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
