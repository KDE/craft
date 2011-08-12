# This package-script is automatically updated by the script win32libsupdater.py
# which can be found in your emerge/bin folder. To update this package, run
# win32libsupdater.py (and commit the results)
# based on revision gitcfc5b700df8db112d62408e5402ba6ed7170a64d

from Package.BinaryPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = 'http://downloads.sourceforge.net/kde-windows'

        for version in [ '0.9.26' ]:
            self.targets[ version ]          = self.getPackage( repoUrl, 'rasqal', version )
            self.targetDigestUrls[ version ] = self.getPackage( repoUrl, 'rasqal', version, '.tar.bz2.sha1' )

        self.defaultTarget = '0.9.26'


    def setDependencies( self ):
        if not utils.envAsBool( 'EMERGE_ENABLE_IMPLICID_BUILDTIME_DEPENDENCIES' ):
            self.buildDependencies[ 'gnuwin32/wget' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/expat' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/yajl' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/libxslt' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/pcre' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/raptor2' ] = 'default'
        self.runtimeDependencies[ 'win32libs-bin/libcurl' ] = 'default'
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
