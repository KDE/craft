# -*- coding: utf-8 -*-
import info

from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.MultiPackager import *
from Package.PackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.4.10'] = 'ftp://ftp.gnupg.org/gcrypt/gnupg/gnupg-1.4.10.tar.bz2'
        self.targetInstSrc['1.4.10'] = 'gnupg-1.4.10'
        self.targetDigests['1.4.10'] = 'fd1b6a5f3b2dd836b598a1123ac257b8f105615d'
        self.defaultTarget = '1.4.10'
        self.options.package.withCompiler = False

    def setDependencies( self ):
        self.hardDependencies['virtual/bin-base'] = 'default'
        
class Package(PackageBase, MultiSource, AutoToolsBuildSystem, MultiPackager):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)        
        MultiPackager.__init__(self)
        self.buildInSource = True

if __name__ == '__main__':
    Package().execute()
