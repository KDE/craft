# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *

# This is an example package for building 

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ '2.0.10' ] = ""
        self.defaultTarget = '2.0.10'
    
    def setDependencies( self ):
        self.dependencies[ 'testing/vym' ] = 'default'
        self.dependencies[ 'libs/runtime' ] = 'default'
    
class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        blacklists = [ NSIPackagerLists.runtimeBlacklist, 'blacklist.txt' ]
        VirtualPackageBase.__init__( self )
        NullsoftInstallerPackager.__init__( self, blacklists=blacklists )
        
        self.defines[ "executable" ] = "bin\\vym.exe"
        self.defines[ "icon" ] = os.path.join( portage.getPackageInstance('testing','vym').imageDir(), "share", "vym", "icons", "vym.ico")
        

if __name__ == '__main__':
    Package().execute()
