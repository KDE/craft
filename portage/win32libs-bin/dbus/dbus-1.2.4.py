from Package.BinaryPackageBase import *
import os
import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        repoUrl = """http://downloads.sourceforge.net/kde-windows"""

        for version in [ '1.2.4-1' ]:
            self.targets[ version ] = self.getPackage( repoUrl, "dbus", version )

        self.defaultTarget = '1.2.4-1'

    def setDependencies( self ):
        self.hardDependencies[ 'virtual/bin-base' ] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package( BinaryPackageBase ):
  def __init__( self ):
    self.subinfo = subinfo()
    BinaryPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
