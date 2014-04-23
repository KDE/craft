import os

import info


# since the cwrsync .zip/installer combination requires admin privileges to install
# cwrsync is repackaged here

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['4.1.0'] = 'http://downloads.sourceforge.net/sourceforge/kde-windows/cwrsync-4.1.0.7z'
        self.targetDigests['4.1.0'] = '7db69d0191aacf5bd0fd64a7b665f55ae78a50ad'
        self.defaultTarget = '4.1.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *

class Package( BinaryPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = os.path.join( "dev-utils", "rsync" )
        BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
