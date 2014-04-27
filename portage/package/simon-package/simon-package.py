# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *

# This is an example package for building

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.simon = portage.getPackageInstance('testing','simon')
        _,gitVersion = self.simon.getPackageVersion() 
        self.svnTargets[ 'git-' + gitVersion  ] = ""
        self.svnTargets[ '0.3.70' ] = ""
        self.defaultTarget = '0.3.70'



    def setDependencies( self ):
        self.dependencies[ 'testing/simon' ] = 'default'
        self.dependencies[ 'kde/kde-workspace' ] = 'default'
        self.dependencies[ 'kde/kdepim-runtime' ] = 'default'
        self.dependencies[ 'libs/runtime' ] = 'default'
        #self.dependencies[ 'kdesupport/phonon-ds9' ] = 'default'
        
class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        blacklists = [ NSIPackagerLists.runtimeBlacklist, 'blacklist.txt', 'blacklist-virtuoso.txt' ]
        NullsoftInstallerPackager.__init__( self, blacklists=blacklists )
        VirtualPackageBase.__init__( self )
        self.scriptname = os.path.join(self.packageDir(),"NullsoftInstaller.nsi")
        self.defines[ "simon-root" ] = self.subinfo.simon.sourceDir()

