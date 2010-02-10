import os
from shells import MSysShell
import info


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['dev-util/msys'] = 'default'
        self.hardDependencies['testing/glib'] = 'default'
        self.hardDependencies['testing/pkg-config'] = 'default'

    def setTargets( self ):
        self.targets['0.40.6'] = 'http://ftp.acc.umu.se/pub/gnome/sources/intltool/0.40/intltool-0.40.6.tar.bz2'
        self.targetInstSrc['0.40.6'] = "intltool-0.40.6"
        self.options.package.withCompiler = False
        
        self.targetMergePath['0.40.6']= "msys";

        self.defaultTarget = '0.40.6'

from Package.PackageBase import *
from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.KDEWinPackager import *;

class Package( PackageBase, MultiSource, AutoToolsBuildSystem, KDEWinPackager):
    def __init__( self ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)
        KDEWinPackager.__init__(self)

        
if __name__ == '__main__':
     Package().execute()
