import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:%s|%s|' % (self.package, "frameworks")

        self.shortDescription = 'an interactive physical simulator'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.buildDependencies['dev-util/extra-cmake-modules'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtdeclarative'] = 'default'
        self.dependencies['libs/qtsvg'] = 'default'
        self.dependencies['frameworks/khtml'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kdelibs4support'] = 'default'
        self.dependencies['frameworks/knewstuff'] = 'default'
        self.dependencies['frameworks/kplotting'] = 'default'
        self.dependencies['win32libs/eigen2'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

