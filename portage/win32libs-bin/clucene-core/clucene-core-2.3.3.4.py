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

        for version in [ '0.9.21b', '2.3.3.4' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'clucene-core', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'clucene-core', version, '.tar.bz2.sha1' )

        self.shortDescription = '''high-performance, full-featured text search engine (required for compiling strigi)'''

        self.defaultTarget = '2.3.3.4'


    def setDependencies( self ):
        if not utils.envAsBool( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'virtual/bin-base' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/boost-thread' ] = 'default'


    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(BinaryPackageBase):
  def __init__(self):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
