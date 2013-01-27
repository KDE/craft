import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:filelight|KDE/4.9|'
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets['4.9.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.9." + ver + "/src/filelight-4.9." + ver + ".tar.xz"
            self.targetInstSrc['4.9.' + ver] = 'filelight-4.9.' + ver
        self.shortDescription = "a graphical representation of your file system"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.runtimeDependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
