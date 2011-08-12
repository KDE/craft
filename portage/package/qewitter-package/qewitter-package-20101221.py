# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *

# This is an example package for building 

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets[ '0.035' ] = ""
        self.defaultTarget = '0.035'
    
    def setDependencies( self ):
        self.dependencies[ 'qt-apps/qewitter' ] = 'default'
        self.dependencies[ 'libs/runtime' ] = 'default'
    
class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        whitelists = [ 'whitelist.txt' ]
        blacklists = [ NSIPackagerLists.runtimeBlacklist, 'blacklist.txt' ]
        VirtualPackageBase.__init__( self )
        NullsoftInstallerPackager.__init__( self, whitelists,blacklists )
        
        self.defines[ "executable" ] = "bin\\qewitter.exe"
        

if __name__ == '__main__':
    Package().execute()
