import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['master'] = 'git://gitorious.org/kdevelop/quanta.git'
        self.defaultTarget = 'master'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['extragear/kdevplatform'] = 'default'
        self.dependencies['extragear/kdevelop'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__(self)


