# -*- coding: utf-8 -*-
import info
import emergePlatform
import os

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['win32libs/automoc'] = 'default'
        if self.options.features.nepomuk:
            self.dependencies['kdesupport/soprano'] = 'default'
        else:
            self.dependencies['kdesupport/strigi'] = 'default'
        self.dependencies['win32libs/boost-program-options']   = 'default'
        self.dependencies['win32libs/libxslt'] = 'default'
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['win32libs/sqlite'] = 'default'
        self.dependencies['win32libs/shared-mime-info'] = 'default'

    def setTargets( self ):
        baseurl = 'http://download.kde.org/stable/akonadi/src/akonadi-%s.tar.bz2'
        for ver in ['1.4.80', '1.4.90', '1.6.0','1.6.2', '1.7.90', '1.9.0', '1.9.2', '1.10.2']:
            self.targets[ver] = baseurl % ver
            self.targetInstSrc[ver] = 'akonadi-' + ver
        self.patchToApply['1.9.0'] = [("akonadi-kde.conf-fix.diff", 1)]
        self.patchToApply['1.9.2'] = [("akonadi-kde.conf-fix.diff", 1), ("akonadi-unused-sockets.diff", 1)]
        self.targetDigests['1.10.2'] = '97660e2a4fc8797ae86ac2981490d3868c6085ff'
        self.patchToApply['1.10.2'] = [("akonadi-kde.conf-fix.diff", 1)]

        self.svnTargets['gitHEAD'] = '[git]kde:akonadi.git'
        self.shortDescription = "a storage service for PIM data and meta data"
        self.defaultTarget = '1.10.2'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        if self.subinfo.options.features.akonadiBackendSqlite:
            self.subinfo.options.configure.defines += (
                    " -DINSTALL_QSQLITE_IN_QT_PREFIX=TRUE"
                    " -DDATABASE_BACKEND=SQLITE " )
        if not self.subinfo.options.features.nepomuk:
            self.subinfo.options.configure.defines += " -DAKONADI_USE_STRIGI_SEARCH=ON"


if __name__ == '__main__':
    Package().execute()
