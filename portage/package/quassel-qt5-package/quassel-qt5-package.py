# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import *
from Packager.NullsoftInstallerPackager import *

# youll need http://nsis.sourceforge.net/WinShell_plug-in

class subinfo( info.infoclass ):
    def setTargets( self ):
        gitVersion = portage.getPackageInstance('extragear','quassel').sourceVersion() 
        self.svnTargets[ gitVersion  ] = ""
        self.targets[ '0.10.0' ] = ""
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
        
        
    def preArchive(self):
        path = os.path.join(self.imageDir(),"plugins")
        for f in os.listdir(path):
            src = os.path.join(path, f)
            if os.path.isdir(src):
                print(src)
                shutil.move(src, os.path.join(self.imageDir(), "bin", f))
        os.rmdir(path);
        
        path = os.path.join(self.imageDir(),"lib","libsnore-qt5")
        for f in os.listdir(path):
            shutil.move(os.path.join(path, f), os.path.join(self.imageDir(), "bin", f))
        os.rmdir(path);
        os.rmdir(os.path.join(self.imageDir(),"lib"))
        
        path = os.path.join(self.imageDir(),"bin")
        for f in os.listdir(path):
            shutil.move(os.path.join(path, f), os.path.join(self.imageDir(), f))
        os.rmdir(path);
        
        return True

