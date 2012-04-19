import os
import sys
import info
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdegraphics-strigi-analyzer'
        self.targets['4.8.0'] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.0/src/kdegraphics-strigi-analyzer-4.8.0.tar.gz'
        self.targetInstSrc['4.8.0'] = 'kdegraphics-strigi-analyzer-4.8.0'
        for ver in ['4.8.1', '4.8.2']:
            self.targets[ver] = "ftp://ftp.kde.org/pub/kde/stable/" + ver + "/src/kdegraphics-strigi-analyzer-" + ver + ".tar.xz"
            self.targetInstSrc[ ver] = 'kdegraphics-strigi-analyzer-' + ver
        self.defaultTarget = '4.8.2'


        self.shortDescription = 'Strigi analyzers for various graphics file formats'


    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kdesupport/strigi'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
