# -*- coding: utf-8 -*-
import info

from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        ver = '3.52.7'
        self.targets[ ver ] = 'http://iodbc.org/downloads/iODBC/libiodbc-3.52.7.tar.gz'
        self.targetInstSrc[ ver ] = 'libiodbc-3.52.7'
        self.defaultTarget = ver
        self.options.package.withCompiler = False

    def setDependencies( self ):
        self.hardDependencies['dev-utils/msys'] = 'default'

class Package(AutoToolsPackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        AutoToolsPackageBase.__init__(self)
        self.buildInSource = True

if __name__ == '__main__':
    Package().execute()
