import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:nepomuk-widgets'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.9.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.9.' + ver + '/src/nepomuk-widgets-4.9.' + ver + '.tar.xz'
            self.targetInstSrc['4.9.' + ver] = 'nepomuk-widgets-4.9.' + ver
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/nepomuk-core'] = 'default'
        self.shortDescription = "Nepomuk GUI components"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
