# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *
#you have to install
#http://nsis.sourceforge.net/Nsis7z_plug-in

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.amarok = portage.getPackageInstance('extragear','amarok')
        _,gitVersion = self.amarok.getPackageVersion() 
        self.svnTargets[ 'git-' + gitVersion  ] = ""
        self.svnTargets[ '2.8.0' ] = ""
        self.defaultTarget = '2.8.0'



    def setDependencies( self ):
        self.dependencies[ 'extragear/amarok' ] = 'default'
        self.dependencies[ 'kde/kde-workspace' ] = 'default'
        # self.dependencies[ 'kdesupport/snorenotify' ] = 'default'
        self.dependencies[ 'libs/runtime' ] = 'default'
        #self.dependencies[ 'win32libs-bin/liblzma' ] = 'default'
        #self.dependencies[ 'kdesupport/hupnp' ] = 'default'#the packages are optional and not installed by default
        self.dependencies[ 'kdesupport/phonon-vlc'] = 'default'
        
class Package( NullsoftInstallerPackager, VirtualPackageBase ):
    def __init__( self, **args ):
        blacklists = [ NSIPackagerLists.runtimeBlacklist, 'blacklist.txt', 'blacklist-virtuoso.txt' ]
        NullsoftInstallerPackager.__init__( self, blacklists=blacklists )
        VirtualPackageBase.__init__( self )
        self.scriptname = os.path.join( emergeSettings.get("Paths",  "KDEGITDIR" ), "amarok", "release_scripts", "windows", "amarok.nsi")
        self.defines[ "kde-version" ] = "4.11.0"

if __name__ == '__main__':
    Package().execute()
