import os
import sys
import info
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:gwenview'
        self.targets['4.8.0'] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.0/src/gwenview-4.8.0.tar.gz'
        self.targetInstSrc['4.8.0'] = 'gwenview-4.8.0'
        for ver in ['4.8.1', '4.8.2']:
            self.targets[ver] = "ftp://ftp.kde.org/pub/kde/stable/" + ver + "/src/gwenview-" + ver + ".tar.xz"
            self.targetInstSrc[ ver] = 'gwenview-' + ver
        self.defaultTarget = '4.8.2'


        self.shortDescription = 'Image viewer for KDE'


    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kde-baseapps'] = 'default'
        self.dependencies['kde/libkipi'] = 'default'
        self.dependencies['win32libs-bin/exiv2'] = 'default'
        self.dependencies['win32libs-bin/jpeg'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
