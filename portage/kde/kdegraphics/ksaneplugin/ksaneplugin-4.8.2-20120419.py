import os
import sys
import info
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:ksaneplugin'
        self.targets['4.8.0'] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.0/src/ksaneplugin-4.8.0.tar.gz'
        self.targetInstSrc['4.8.0'] = 'ksaneplugin-4.8.0'
        for ver in ['4.8.1', '4.8.2']:
            self.targets[ver] = "ftp://ftp.kde.org/pub/kde/stable/" + ver + "/src/ksaneplugin-" + ver + ".tar.xz"
            self.targetInstSrc[ ver] = 'ksaneplugin-' + ver
        self.defaultTarget = '4.8.2'


        self.shortDescription = 'This is a KScan plugin that implements the scanning through libksane'


    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kde/libksane'] = 'default'


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
