import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:nepomuk-core|KDE/4.9|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.9.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.9.' + ver + '/src/nepomuk-core-4.9.' + ver + '.tar.xz'
            self.targetInstSrc['4.9.' + ver] = 'nepomuk-core-4.9.' + ver
            
        self.patchToApply[ '4.9.0' ] = [("qtest.diff",1)]
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kdesupport/soprano'] = 'default'
        self.dependencies['kdesupport/strigi'] = 'default'
        self.dependencies['data/shared-desktop-ontologies'] = 'default'
        self.dependencies['kde/kdelibs'] = 'default'
        self.shortDescription = "Nepomuk core libraries"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
