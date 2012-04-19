import os
import sys
import info
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:libksane'
        self.targets['4.8.0'] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.0/src/libksane-4.8.0.tar.bz2'
        self.targetInstSrc['4.8.0'] = 'libksane-4.8.0'
        for ver in ['4.8.1', '4.8.2']:
            self.targets[ver] = "ftp://ftp.kde.org/pub/kde/stable/" + ver + "/src/libksane-" + ver + ".tar.xz"
            self.targetInstSrc[ ver] = 'libksane-' + ver
        self.defaultTarget = '4.8.2'


        self.shortDescription = 'libksane is an image scanning library that provides a QWidget that contains all the logic needed to interface a sacanner.'


    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
