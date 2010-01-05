# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.3/kdeedu'
        for ver in ['91', '95', '98']:
          self.targets['4.2.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.2.' + ver + '/src/kdeedu-4.2.' + ver + '.tar.bz2'
          self.targetInstSrc['4.2.' + ver] = 'kdeedu-4.2.' + ver
        self.patchToApply['4.2.95'] = ('kdeedu-kmplot.diff', 0)
        for ver in ['0', '1', '2', '3', '4']:
          self.targets['4.3.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.3.' + ver + '/src/kdeedu-4.3.' + ver + '.tar.bz2'
          self.targetInstSrc['4.3.' + ver] = 'kdeedu-4.3.' + ver
        self.patchToApply['4.3.0'] = ('1011613.diff', 0)
        self.patchToApply['4.3.0'] = ('kdeedu-kmplot.diff', 0)
        self.patchToApply['4.3.3'] = ('khangman.diff', 1)
          
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.3/kdebase-runtime'] = 'default'

        self.softDependencies['kdesupport/eigen2'] = 'default'
        self.hardDependencies['win32libs-bin/cfitsio'] = 'default'
        self.hardDependencies['win32libs-bin/libnova'] = 'default'
        self.hardDependencies['win32libs-bin/openbabel'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
