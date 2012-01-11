import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdeplasma-addons|KDE/4.8|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.8.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.8." + ver + "/src/kdeplasma-addons-4.8." + ver + ".tar.bz2"
            self.targetInstSrc['4.8.' + ver] = 'kdeplasma-addons-4.8.' + ver
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kde-workspace'] = 'default'
        self.shortDescription = "All kind of addons to improve your Plasma experience"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
