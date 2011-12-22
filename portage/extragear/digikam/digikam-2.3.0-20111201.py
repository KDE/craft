# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:digikam'
        for ver in ['1.0.0', '1.1.0', '1.6.0', '1.7.0', '2.0.0', '2.1.1','2.3.0']:
            self.targets[ver] = 'http://downloads.sourceforge.net/project/digikam/digikam/' + ver + '/digikam-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'digikam-' + ver

        self.patchToApply['1.1.0'] = ('digikam-1.1.0.diff', 1)
        self.patchToApply['1.7.0'] = ('digikam-1.7.0-20101219.diff', 1)
        self.patchToApply['2.0.0'] = ('digikam-2.0.0-20110825.diff', 1)

        self.options.configure.defines = "-DENABLE_GPHOTO2=OFF"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['virtual/kde-runtime'] = 'default'
        self.dependencies['kde/libkdcraw'] = 'default'
        self.dependencies['kde/libkexiv2'] = 'default'
        self.dependencies['kde/libkipi'] = 'default'
        self.dependencies['kde/marble'] = 'default'
        self.dependencies['win32libs-bin/lcms'] = 'default'
        self.dependencies['win32libs-bin/tiff'] = 'default'
        self.dependencies['win32libs-bin/gettext'] = 'default'
        self.dependencies['win32libs-bin/opencv'] = 'default'
        self.buildDependencies['dev-util/gettext-tools'] = 'default'        
        self.shortDescription = "an advanced digital photo management application"

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.make.supportsMultijob = False

if __name__ == '__main__':
    Package().execute()
