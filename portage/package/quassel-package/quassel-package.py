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
        self.targets[ '0.11.0-1'] = ""
        self.defaultTarget = '0.11.0-1'

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
        
        
    def preArchive(self):
        path = os.path.join(self.imageDir(),"plugins")
        for f in os.listdir(path):
            src = os.path.join(path, f)
            if os.path.isdir(src):
                utils.moveFile(src, os.path.join(self.imageDir(), "bin", f))
        utils.rmtree(path);
        

        utils.moveDir( os.path.join(self.imageDir(),"lib","libsnore-qt5"), os.path.join(self.imageDir(), "bin"))
        utils.rmtree(os.path.join(self.imageDir(),"lib"))
        
        path = os.path.join(self.imageDir(),"bin")
        for f in os.listdir(path):
            utils.moveFile(os.path.join(path, f), os.path.join(self.imageDir(), f))
        utils.rmtree(path);
        
        return True

