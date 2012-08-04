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
        self.targets['5.5.25a'] = 'ftp://ftp.fu-berlin.de/unix/databases/mysql/Downloads/MySQL-5.5/mysql-5.5.25a.tar.gz'
        self.targetDigests['5.5.25a'] = '85dfea413a7d5d2733a40f9dd79cf2320302979f'
        self.targetInstSrc[ '5.5.25a' ] = "mysql-5.5.25a"
        self.patchToApply['5.5.25a'] = ("mysql-5.5.25a-20120804.diff",1)
        self.defaultTarget = '5.5.25a'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DWITH_UNIT_TESTS=OFF -DENABLED_PROFILING=OFF -DINSTALL_SQLBENCHDIR= -DINSTALL_MYSQLTESTDIR= -DWITH_ZLIB=system -DWITH_SSL=system"

if __name__ == '__main__':
    Package().execute()
