import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "[git]kde:calligra"
        for ver in ['2.3.74']:
            self.targets[ver] = 'ftp://ftp.kde.org/pub/kde/unstable/calligra-' + ver + '/calligra-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'calligra-' + ver
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/lcms'] = 'default'
        self.hardDependencies['kde/kdepimlibs'] = 'default'
        self.hardDependencies['kde/kde-runtime'] = 'default'
        self.hardDependencies['kdesupport/eigen2'] = 'default'
        self.softDependencies['kdesupport/qca'] = 'default'
        self.softDependencies['testing/gsl'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF "

if __name__ == '__main__':
    Package().execute()