# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/graphics/digikam'
        self.targets['0.10.0'] = 'http://digikam3rdparty.free.fr/0.10.x-releases/digikam-0.10.0.tar.bz2'
        self.targetInstSrc['0.10.0'] = 'digikam-0.10.0'
        for ver in ['beta1', 'beta3', 'beta4', 'beta5']:
            self.targets['1.0.0-' + ver] = 'http://downloads.sourceforge.net/project/digikam/digikam/1.0.0-' + ver + '/digikam-1.0.0-' + ver + '.tar.bz2'
            self.targetInstSrc['1.0.0-' + ver] = 'digikam-1.0.0-' + ver
        
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
