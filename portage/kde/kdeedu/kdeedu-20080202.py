import base
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdeedu'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeedu'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdeedu-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdeedu-4.0.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'

        self.softDependencies['kdesupport/eigen2'] = 'default'
        self.hardDependencies['win32libs-bin/cfitsio'] = 'default'
        self.hardDependencies['win32libs-bin/libnova'] = 'default'
        self.hardDependencies['win32libs-bin/openbabel'] = 'default'
        self.hardDependencies['win32libs-bin/boost'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF"

if __name__ == '__main__':
    Package().execute()
