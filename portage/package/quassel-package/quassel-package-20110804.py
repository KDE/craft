# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *

# youll need http://nsis.sourceforge.net/WinShell_plug-in

class subinfo( info.infoclass ):
    def setTargets( self ):
        gitVersion = portage.getPackageInstance('extragear','quassel').sourceVersion() 
        self.svnTargets[ gitVersion  ] = ""
        self.targets[ '0.10.0-1' ] = ""
        self.defaultTarget = gitVersion

    def setDependencies( self ):
        self.dependencies[ 'extragear/quassel' ] = 'default'
        self.dependencies[ 'libs/runtime' ] = 'default'
        
class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        whitelists = [ 'whitelist.txt' ]
        blacklists = [ NSIPackagerLists.runtimeBlacklist, 'blacklist.txt' ]
        VirtualPackageBase.__init__( self )
        NullsoftInstallerPackager.__init__( self, whitelists,blacklists )
        self.scriptname = os.path.join(self.packageDir(),"NullsoftInstaller.nsi")

