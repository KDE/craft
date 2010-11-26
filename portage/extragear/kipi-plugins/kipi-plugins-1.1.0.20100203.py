# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/graphics/kipi-plugins'
        for ver in ['0.2.0', '0.3.0', '0.5.0', '0.6.0', '0.7.0', '0.8.0', '1.0.0', '1.1.0', '1.6.0']:
            self.targets[ ver ] = "http://downloads.sourceforge.net/project/kipi/kipi-plugins/" + ver + "/kipi-plugins-" + ver + ".tar.bz2"
            self.targetInstSrc[ ver ] = 'kipi-plugins-' + ver
        self.patchToApply[ '0.7.0' ] = ( 'kipi-twain-stable.diff', 0 )
        self.patchToApply[ '0.8.0' ] = ( 'kipi-plugins-0.8.0-20091106.diff', 1 )
        self.patchToApply[ '1.1.0' ] = ( 'kipi-plugins-1.1.0.diff', 1 )
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['virtual/kdebase-runtime'] = 'default'
        self.dependencies['virtual/kdegraphics'] = 'default'
        self.dependencies['win32libs-bin/expat'] = 'default'
        self.dependencies['win32libs-bin/gettext'] = 'default'
        self.buildDependencies['dev-util/gettext-tools'] = 'default'

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
