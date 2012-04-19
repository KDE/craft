import os
import sys
import info
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:okular'
        self.targets['4.8.0'] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.0/src/okular-4.8.0.tar.bz2'
        self.targetInstSrc['4.8.0'] = 'okular-4.8.0'
        for ver in ['4.8.1', '4.8.2']:
            self.targets[ver] = "ftp://ftp.kde.org/pub/kde/stable/" + ver + "/src/okular-" + ver + ".tar.xz"
            self.targetInstSrc[ ver] = 'okular-' + ver
        self.defaultTarget = '4.8.2'


        self.patchToApply['4.8.0'] = [('replace-usage-of-unportable-mkdtemp-with-KTempDir-update.patch',1)]

        self.homepage = 'http://okular.kde.org/'

        self.shortDescription = 'KDE document viewer.'


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


from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
