import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kfloppy|KDE/4.8|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.8.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.8." + ver + "/src/kfloppy-4.8." + ver + ".tar.bz2"
            self.targetInstSrc['4.8.' + ver] = 'kfloppy-4.8.' + ver
        self.shortDescription = "a utility to format floppy disks"
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
