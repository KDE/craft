# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/openssl'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'
        self.buildDependencies['dev-util/winflexbison'] = 'default'

        
    def setTargets( self ):
        self.targets['5.5.25a'] = 'ftp://ftp.fu-berlin.de/unix/databases/mysql/Downloads/MySQL-5.5/mysql-5.5.25a.tar.gz'
        self.targetDigests['5.5.25a'] = '85dfea413a7d5d2733a40f9dd79cf2320302979f'
        self.targetInstSrc[ '5.5.25a' ] = "mysql-5.5.25a"
        self.patchToApply['5.5.25a'] = [("mysql-5.5.25a-20120804.diff",1)]
        self.defaultTarget = '5.5.25a'
         

class Package( CMakePackageBase ):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.defines = "-DWITH_UNIT_TESTS=OFF -DENABLED_PROFILING=OFF -DINSTALL_SQLBENCHDIR= -DINSTALL_MYSQLTESTDIR= -DWITH_ZLIB=system -DWITH_SSL=system"

