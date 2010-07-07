# -*- coding: utf-8 -*-
import info

from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.MultiPackager import *
from Package.PackageBase import *
from shells import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['1.0.21'] = 'http://www.mega-nerd.com/libsndfile/files/libsndfile-1.0.21.tar.gz'
        self.targetInstSrc['1.0.21'] = 'libsndfile-1.0.21'
        self.defaultTarget = '1.0.21'
        self.options.package.withCompiler = False

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/wget'] = 'default'
        self.hardDependencies['dev-util/msys'] = 'default'
        
class Package(PackageBase, MultiSource, AutoToolsBuildSystem, MultiPackager):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        MultiSource.__init__(self)
        AutoToolsBuildSystem.__init__(self)        
        MultiPackager.__init__(self)
        self.buildInSource = True
        self.subinfo.options.configure.defines = " --docdir=" + MSysShell().toNativePath(self.imageDir()[2:])

if __name__ == '__main__':
    Package().execute()
