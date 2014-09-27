import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['frameworks'] = '[git]kde:kgeography|frameworks'

        self.shortDescription = 'a geography trainer'
        self.defaultTarget = 'frameworks'

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['kde/kxmlgui'] = 'default'
        self.dependencies['frameworks/kwidgetsaddons'] = 'default'
        self.dependencies['frameworks/kcoreaddons'] = 'default'
        self.dependencies['kde/kconfigwidgets'] = 'default'
        self.dependencies['kde/ki18n'] = 'default'
        self.dependencies['kde/kitemviews'] = 'default'
        self.dependencies['kde/kiconthemes'] = 'default'
        self.dependencies['kde/kservice'] = 'default'
        self.dependencies['kde/kdoctools'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

