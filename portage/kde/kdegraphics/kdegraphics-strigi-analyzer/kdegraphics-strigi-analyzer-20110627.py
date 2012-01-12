import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdegraphics-strigi-analyzer|KDE/4.8|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.8.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.8." + ver + "/src/kdegraphics-strigi-analyzer-4.8." + ver + ".tar.bz2"
            self.targetInstSrc['4.8.' + ver] = 'kdegraphics-strigi-analyzer-4.8.' + ver
        self.shortDescription = "Strigi analyzers for various graphics file formats"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['win32libs-bin/tiff'] = 'default'
        self.dependencies['kdesupport/strigi'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
