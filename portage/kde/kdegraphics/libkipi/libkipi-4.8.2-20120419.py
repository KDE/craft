import os
import sys
import info
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:libkipi'
        self.targets['4.8.0'] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.0/src/libkipi-4.8.0.tar.gz'
        self.targetInstSrc['4.8.0'] = 'libkipi-4.8.0'
        for ver in ['4.8.1', '4.8.2']:
            self.targets[ver] = "ftp://ftp.kde.org/pub/kde/stable/" + ver + "/src/libkipi-" + ver + ".tar.xz"
            self.targetInstSrc[ ver] = 'libkipi-' + ver
        self.defaultTarget = '4.8.2'


        self.shortDescription = 'Libkipi is an interface to use kipi-plugins from a KDE image management program like digiKam.'


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
