import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.8.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.8." + ver + "/src/svgpart-4.8." + ver + ".tar.bz2"
            self.targetInstSrc['4.8.' + ver] = 'svgpart-4.8.' + ver
        self.svnTargets['gitHEAD'] = '[git]kde:svgpart|KDE/4.8|'
        self.shortDescription = "A svg kpart"
        self.defaultTarget = 'gitHEAD'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
