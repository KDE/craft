import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:zanshin'
        self.svnTargets['0.2-beta1'] = 'http://files.kde.org/zanshin/zanshin-0.1.81.tar.bz2'
        self.description = "a powerful yet simple application for managing your day to day actions"
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdepimlibs'] = 'default'

class Package(CMakePackageBase):
    def __init__( self):
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
