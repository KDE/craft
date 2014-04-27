# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *

# This is an example package for building 

class subinfo( info.infoclass ):
    def setTargets( self ):
        _,gitVersion = portage.getPackageInstance('qt-apps','qewitter').getPackageVersion() 
        self.svnTargets[ 'git-' + gitVersion  ] = ""
        self.svnTargets[ '0.11pre' ] = ""
        self.defaultTarget = '0.11pre'
    
    def setDependencies( self ):
        self.dependencies[ 'qt-apps/qewitter' ] = 'default'
        self.dependencies[ 'libs/runtime' ] = 'default'
    
class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        whitelists = [ 'whitelist.txt' ]
        blacklists = [ NSIPackagerLists.runtimeBlacklist, 'blacklist.txt' ]
        VirtualPackageBase.__init__( self )
        NullsoftInstallerPackager.__init__( self, whitelists,blacklists )
        
        self.defines[ "executable" ] = "bin\\qewitter.exe"
        self.defines[ "icon" ] = os.path.join(portage.getPackageInstance('qt-apps','qewitter').sourceDir(),"data","qewitter.ico")
        

