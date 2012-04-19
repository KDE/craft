import os
import sys
import info
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:ksnapshot'
        self.targets['4.8.0'] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.0/src/ksnapshot-4.8.0.tar.bz2'
        self.targetInstSrc['4.8.0'] = 'ksnapshot-4.8.0'
        for ver in ['4.8.1', '4.8.2']:
            self.targets[ver] = "ftp://ftp.kde.org/pub/kde/stable/" + ver + "/src/ksnapshot-" + ver + ".tar.xz"
            self.targetInstSrc[ ver] = 'ksnapshot-' + ver
        self.defaultTarget = '4.8.2'


        self.shortDescription = 'A handy utility primarily designed for taking screenshots'


    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kde/libkipi'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
