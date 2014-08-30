import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:%s|%s|' % (self.package, "master")

        self.shortDescription = 'the educational support libraries'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['kde/kconfig'] = 'default'
        self.dependencies['kde/ki18n'] = 'default'
        self.dependencies['kde/karchive'] = 'default'
        self.dependencies['kde/kio'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

