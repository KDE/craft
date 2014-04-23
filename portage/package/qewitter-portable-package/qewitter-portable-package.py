# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *
from Packager.PortablePackager import *

# This is an example package for building

class subinfo( info.infoclass ):
    def setTargets( self ):
        _,gitVersion = portage.getPackageInstance('qt-apps','qewitter').getPackageVersion() 
        self.svnTargets[ 'git-' + gitVersion  ] = ""
        self.svnTargets[ '0.11' ] = ""
        self.defaultTarget = '0.11'

    def setDependencies( self ):
        self.dependencies[ 'qt-apps/qewitter' ] = 'default'
        self.dependencies[ 'kdesupport/snorenotify' ] = 'default'
        self.dependencies[ 'libs/runtime' ] = 'default'
        
class Package( PortablePackager, VirtualPackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        whitelists = [ 'whitelist.txt' ]
        blacklists = [ NSIPackagerLists.runtimeBlacklist, 'blacklist.txt' ]
        PortablePackager.__init__( self, whitelists ,blacklists )
        VirtualPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
