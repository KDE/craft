# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *

# This is an example package for building

class subinfo( info.infoclass ):
    def setTargets( self ):
        _,gitVersion = portage.getPackageInstance('extragear','rekonq').getPackageVersion()
        self.svnTargets[ 'git-' + gitVersion ] = ""
        self.svnTargets[ '1.1' ] = ""
        self.defaultTarget = '1.1'
    
    def setDependencies( self ):
        self.dependencies[ 'extragear/rekonq' ] = 'default'
    
class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        # whitelists = [ 'whitelist.txt' ]
        # blacklists = [ NSIPackagerLists.runtimeBlacklist, 'blacklist.txt' ]
        VirtualPackageBase.__init__( self )
        # NullsoftInstallerPackager.__init__( self, whitelists,blacklists )
        NullsoftInstallerPackager.__init__( self )
        
        self.defines[ "executable" ] = "bin\\rekonq.exe"
        # self.defines[ "icon" ] = os.path.join(portage.getPackageInstance('extragear','rekonq').sourceDir(),"icons","rekonq.ico")
        

if __name__ == '__main__':
    Package().execute()
