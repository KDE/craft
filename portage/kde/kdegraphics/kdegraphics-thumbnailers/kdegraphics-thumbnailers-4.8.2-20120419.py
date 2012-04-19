import os
import sys
import info
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdegraphics-thumbnailers'
        self.targets['4.8.0'] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.0/src/kdegraphics-thumbnailers-4.8.0.tar.gz'
        self.targetInstSrc['4.8.0'] = 'kdegraphics-thumbnailers-4.8.0'
        for ver in ['4.8.1', '4.8.2']:
            self.targets[ver] = "ftp://ftp.kde.org/pub/kde/stable/" + ver + "/src/kdegraphics-thumbnailers-" + ver + ".tar.xz"
            self.targetInstSrc[ ver] = 'kdegraphics-thumbnailers-' + ver
        self.defaultTarget = '4.8.2'


        self.shortDescription = 'Thumbnailers for various graphics file formats'


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
