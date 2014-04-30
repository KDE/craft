# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *

# youll need http://nsis.sourceforge.net/WinShell_plug-in

class subinfo( info.infoclass ):
    def setTargets( self ):
        for pack in installdb.getInstalledPackages('extragear','quassel'):
            gitVersion = pack.getRevision()
            if not gitVersion is None:
                self.svnTargets[ gitVersion  ] = ""
                self.defaultTarget = gitVersion
        self.targets[ '0.10.0' ] = ""
        self.defaultTarget = '0.10.0'

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

