import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kstars|frameworks|'

        self.shortDescription = 'a desktop planetarium'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        #self.buildDependencies['win32libs/cfitsio'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtdeclarative'] = 'default'
        self.dependencies['libs/qtsvg'] = 'default'
        self.dependencies['kde/kconfig'] = 'default'
        self.dependencies['kde/kdoctools'] = 'default'
        self.dependencies['kde/kguiaddons'] = 'default'
        self.dependencies['kde/kwidgetsaddons'] = 'default'
        self.dependencies['kde/knewstuff'] = 'default'
        self.dependencies['kde/kdbusaddons'] = 'default'
        self.dependencies['kde/ki18n'] = 'default'
        self.dependencies['kde/kinit'] = 'default'
        self.dependencies['kde/kjobwidgets'] = 'default'
        self.dependencies['kde/kio'] = 'default'
        self.dependencies['kde/kwindowsystem'] = 'default'
        self.dependencies['kde/kxmlgui'] = 'default'
        self.dependencies['kde/kplotting'] = 'default'
        self.dependencies['kde/ktexteditor'] = 'default'
        self.dependencies['kde/kiconthemes'] = 'default'
        self.dependencies['win32libs/eigen3'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

