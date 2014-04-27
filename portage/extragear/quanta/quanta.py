import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/kdevelop/quanta.git'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde/kde-runtime'] = 'default'
        self.hardDependencies['extragear/kdevplatform'] = 'default'
        self.hardDependencies['extragear/kdevelop'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()

