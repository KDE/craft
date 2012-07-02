import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = "[git]kde:calligra|calligra/2.4"
        for ver in ['2.4.91']:
            self.targets[ver] = 'ftp://ftp.kde.org/pub/kde/unstable/calligra-' + ver + '/calligra-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'calligra-' + ver
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde/kde-runtime'] = 'default'
        self.hardDependencies['win32libs-bin/boost'] = 'default'
        self.hardDependencies['win32libs-bin/lcms2'] = 'default'
        self.hardDependencies['kdesupport/eigen2'] = 'default'
        self.hardDependencies['kdesupport/soprano'] = 'default'
        self.hardDependencies['win32libs-bin/exiv2'] = 'default'
        self.hardDependencies['win32libs-sources/librdf-src'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DBUILD_doc=OFF -DTINY=off -DBUILD_active=off -DBUILD_mobile=off -DBUILD_kexi=off -DWITH_WPG=off"

if __name__ == '__main__':
    Package().execute()