# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/graphics/digikam'
        for ver in ['1.0.0', '1.1.0']:
            self.targets[ver] = 'http://downloads.sourceforge.net/project/digikam/digikam/' + ver + '/digikam-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'digikam-' + ver
        for ver in ['beta1', 'beta3', 'beta4', 'beta5']:
            self.targets['1.0.0-' + ver] = 'http://downloads.sourceforge.net/project/digikam/digikam/1.0.0-' + ver + '/digikam-1.0.0-' + ver + '.tar.bz2'
            self.targetInstSrc['1.0.0-' + ver] = 'digikam-1.0.0-' + ver
            
        self.patchToApply['1.1.0'] = ('digikam-1.1.0.diff', 1)
        
        self.svnTargets['branch-0.10.0'] = 'branches/extragear/graphics/digikam/0.10.0-trunk'
        self.options.configure.defines = "-DENABLE_GPHOTO2=OFF"
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kde/kdegraphics'] = 'default'
        self.hardDependencies['win32libs-bin/lcms'] = 'default'
        self.hardDependencies['win32libs-bin/gettext'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
