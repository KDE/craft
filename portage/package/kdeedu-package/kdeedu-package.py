# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *

# This is an example package for building

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['4.9.1', '4.9.2', '4.9.3', '4.9.4']:
          self.svnTargets[ ver ] = ''

        self.defaultTarget = '4.9.0'
    
    def setDependencies( self ):
        self.dependencies[ 'kde/kdeedu' ] = 'default'
    
class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        # whitelists = [ 'whitelist.txt' ]
        # blacklists = [ NSIPackagerLists.runtimeBlacklist, 'blacklist.txt' ]
        VirtualPackageBase.__init__( self )
        self.scriptname = os.path.join(self.packageDir(),"NullsoftInstaller.nsi")
        # NullsoftInstallerPackager.__init__( self, whitelists,blacklists )
        NullsoftInstallerPackager.__init__( self )
        

if __name__ == '__main__':
    Package().execute()
