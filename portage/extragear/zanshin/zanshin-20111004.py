import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:zanshin'
        releases = [ '0.1.81','0.1.91','0.2' ]
        for ver in releases:
            self.targets[ ver ] = 'http://files.kde.org/zanshin/zanshin-' +  ver  + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'zanshin-' + ver
        self.shortDescription = "a powerful yet simple application for managing your day to day actions"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['virtual/kdepimlibs'] = 'default'

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
