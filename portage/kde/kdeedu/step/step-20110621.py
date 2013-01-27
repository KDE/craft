import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:step|KDE/4.9|'
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets['4.9.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.9." + ver + "/src/step-4.9." + ver + ".tar.xz"
            self.targetInstSrc['4.9.' + ver] = 'step-4.9.' + ver
        self.shortDescription = 'an interactive physical simulator'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kdesupport/eigen2'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
