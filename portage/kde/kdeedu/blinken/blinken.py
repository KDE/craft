import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['frameworks'] = '[git]kde:blinken|frameworks'

        self.shortDescription = 'a memory enhancement game'
        self.defaultTarget = 'frameworks'

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtsvg'] = 'default'
        self.dependencies['kde/ki18n'] = 'default'
        self.dependencies['kde/kxmlgui'] = 'default'
        self.dependencies['kde/kguiaddons'] = 'default'
        self.dependencies['kde/kdoctools'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

