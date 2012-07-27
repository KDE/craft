import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:okular|KDE/4.9|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.9.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.9." + ver + "/src/okular-4.9." + ver + ".tar.xz"
            self.targetInstSrc['4.9.' + ver] = 'okular-4.9.' + ver
        self.shortDescription = 'KDE document viewer.'
        self.defaultTarget = 'gitHEAD'
        self.homepage = 'http://okular.kde.org/'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.buildDependencies['win32libs-bin/chm'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['kdesupport/poppler'] = 'default'
        self.dependencies['kdesupport/qimageblitz'] = 'default'
        self.dependencies['win32libs-bin/tiff'] = 'default'
        self.dependencies['win32libs-bin/djvu'] = 'default'
        self.dependencies['win32libs-bin/zlib'] = 'default'
        self.dependencies['win32libs-bin/freetype'] = 'default'
        self.dependencies['win32libs-bin/libspectre'] = 'default'
        self.dependencies['win32libs-bin/ebook-tools'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
