# -*- coding: utf-8 -*-
import info

from Source.MultiSource import *
from BuildSystem.AutoToolsBuildSystem import *
from Packager.MultiPackager import *
from Package.PackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = '3.52.7'
        self.targets[ ver ] = 'http://iodbc.org/downloads/iODBC/libiodbc-3.52.7.tar.gz'
        self.targetInstSrc[ ver ] = 'libiodbc-3.52.7'
        self.defaultTarget = ver
        self.options.package.withCompiler = False

    def setDependencies( self ):
        self.hardDependencies['dev-utils/msys'] = 'default'
        
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
