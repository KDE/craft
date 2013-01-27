import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:ark|KDE/4.9|'
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets['4.9.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.9." + ver + "/src/ark-4.9." + ver + ".tar.xz"
            self.targetInstSrc['4.9.' + ver] = 'ark-4.9.' + ver
        self.shortDescription = "KDE's file archiver"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-baseapps'] = 'default' # libkonq is needed
        self.dependencies['kdesupport/qjson'] = 'default'
        self.dependencies['win32libs-bin/libzip'] = 'default'
        self.dependencies['win32libs-bin/libbzip2'] = 'default'
        self.dependencies['win32libs-bin/zlib'] = 'default'
        self.dependencies['win32libs-bin/libarchive'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
