# -*- coding: utf-8 -*-
import info
import os
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['win32libs-bin/openssl'] = 'default'
        self.hardDependencies['win32libs-bin/zlib'] = 'default'
        self.buildDependencies["gnuwin32/bison"] = "default"

        
    def setTargets( self ):
        self.targets['5.5.20'] = 'ftp://ftp.fu-berlin.de/unix/databases/mysql/Downloads/MySQL-5.5/mysql-5.5.20.tar.gz'
        self.targetDigests['5.5.20'] = 'd5066327c41ac5a338ca0bb748e50bc4e1902442'
        self.targetInstSrc[ '5.5.20' ] = "mysql-5.5.20"
        self.patchToApply['5.5.20'] = ("mysql-5.5.20-20120116.diff",1)
        self.defaultTarget = '5.5.20'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DWITH_UNIT_TESTS=OFF -DENABLED_PROFILING=OFF -DINSTALL_SQLBENCHDIR= -DINSTALL_MYSQLTESTDIR= -DWITH_ZLIB=system -DWITH_SSL=system"

if __name__ == '__main__':
    Package().execute()
