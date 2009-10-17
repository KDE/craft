# -*- coding: utf-8 -*-
import info

from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.MultiPackager import *
from Package.PackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.7'] = 'ftp://ftp.gnupg.org/gcrypt/libgpg-error/libgpg-error-1.7.tar.bz2'
        self.targetInstSrc['1.7'] = 'libgpg-error-1.7'
        self.patchToApply['1.7'] = ('libgpg-error-1.7-20091017.diff', 1)
        self.defaultTarget = '1.7'
        self.options.package.withCompiler = False

    def setDependencies( self ):
        self.hardDependencies['testing/gnupg-src'] = 'default'
        self.hardDependencies['gnuwin32/wget'] = 'default'
        
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
