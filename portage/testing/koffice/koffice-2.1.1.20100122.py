# -*- coding: utf-8 -*-

import os
import utils
import info

class subinfo(info.infoclass):
    def setTargets( self ):
	self.svnTargets['gitHEAD'] = "[git]kde:kate"
        for ver in ['2.0.82', '2.0.83', '2.0.91']:
            self.targets[ver] = 'ftp://ftp.kde.org/pub/kde/unstable/koffice-' + ver + '/src/koffice-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'koffice-' + ver
        for ver in ['2.1.0', '2.1.1', '2.3.0']:
            self.targets[ver] = 'ftp://ftp.kde.org/pub/kde/stable/koffice-' + ver + '/src/koffice-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'koffice-' + ver
        self.patchToApply['2.0.0'] = ('koffice-2.0.0.diff', 0)
        self.patchToApply['2.0.82'] = ('koffice-2.0.82.diff', 0)
        self.patchToApply['2.0.83'] = ('koffice-2.0.83.diff', 1)
        self.patchToApply['2.0.91'] = ('koffice-2.0.91.diff', 1)
        self.patchToApply['2.1.0'] = ('koffice-2.1.0.diff', 1)
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.hardDependencies['win32libs/lcms'] = 'default'
        self.hardDependencies['kde/kdepimlibs'] = 'default'
        self.hardDependencies['kde/kde-runtime'] = 'default'
#        self.hardDependencies['kdesupport/eigen'] = 'default'
        self.hardDependencies['kdesupport/eigen2'] = 'default'
        self.softDependencies['kdesupport/qca'] = 'default'
        self.softDependencies['testing/gsl'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
