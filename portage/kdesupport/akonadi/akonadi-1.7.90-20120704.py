# -*- coding: utf-8 -*-
import info
import emergePlatform
import os

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['win32libs/automoc'] = 'default'
        self.dependencies['win32libs/boost-program-options']   = 'default'
        self.dependencies['win32libs/libxslt'] = 'default'
        self.dependencies['libs/qt'] = 'default'
        self.dependencies['win32libs/sqlite'] = 'default'
        self.dependencies['win32libs/shared-mime-info'] = 'default'
        if self.options.features.nepomuk:
            self.dependencies['kdesupport/soprano'] = 'default'

    def setTargets( self ):
        baseurl = 'http://download.kde.org/stable/akonadi/src/akonadi-%s.tar.bz2'
        for ver in ['1.10.2','1.10.80', '1.12.1', '1.13.0']:
            self.targets[ver] = baseurl % ver
            self.targetInstSrc[ver] = 'akonadi-' + ver
        for ver in ['1.10.3']:
            self.targets[ver] = baseurl % (ver + "-1")
            self.targetInstSrc[ver] = 'akonadi-' + ver

        self.targetDigests['1.10.2'] = '97660e2a4fc8797ae86ac2981490d3868c6085ff'
        self.targetDigests['1.10.3'] = '701fbdde01a2787ec47fc085da02ad6238cf3b92'
        self.targetDigests['1.10.80'] = '016ff1d137af37dc1a295958e612cfd92075c3f8'
        self.targetDigests['1.12.1'] = '1ad560a83f08521592b1041c49b5415ffbb2581b'
        self.targetDigests['1.13.0'] = '9d594b5840e2e5d90057a7e5d8545004a3476bc0'

        self.patchToApply['1.10.2'] = [("akonadi-kde.conf-fix.diff", 1)]
        self.patchToApply['1.10.3'] = [("akonadi-kde.conf-fix.diff", 1)]
        self.patchToApply['1.10.80'] = [("akonadi-kde.conf-fix-1.10.80.diff", 1)]
        self.patchToApply['1.12.1'] = [("akonadi-1.12.1-20140419.diff", 1), ("akonadi-kde.conf-fix-1.12.1.diff", 1)]
        self.patchToApply['1.13.0'] = [("0001-FindSqlite-Use-CMAKE_FLAGS-the-right-way-in-try_comp.patch", 1), ("akonadi-1.13-fixes.diff", 1), ("akonadi-kde.conf-fix-1.13.0.diff", 1)]
        self.patchToApply['gitHEAD'] = [("akonadi-kde.conf-fix-1.12.1.diff", 1)]

        self.svnTargets['gitHEAD'] = '[git]kde:akonadi.git'
        self.shortDescription = "a storage service for PIM data and meta data"
        self.defaultTarget = '1.13.0'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        if self.subinfo.options.features.akonadiBackendSqlite or self.subinfo.options.features.nomysql:
            self.subinfo.options.configure.defines += (
                    " -DINSTALL_QSQLITE_IN_QT_PREFIX=TRUE"
                    " -DDATABASE_BACKEND=SQLITE " )
        if not self.subinfo.options.features.nepomuk:
            self.subinfo.options.configure.defines += " -DWITH_SOPRANO=FALSE"


if __name__ == '__main__':
    Package().execute()
