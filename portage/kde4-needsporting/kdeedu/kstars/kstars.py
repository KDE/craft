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
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kdoctools'] = 'default'
        self.dependencies['frameworks/kguiaddons'] = 'default'
        self.dependencies['frameworks/kwidgetsaddons'] = 'default'
        self.dependencies['frameworks/knewstuff'] = 'default'
        self.dependencies['frameworks/kdbusaddons'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['frameworks/kinit'] = 'default'
        self.dependencies['frameworks/kjobwidgets'] = 'default'
        self.dependencies['frameworks/kio'] = 'default'
        self.dependencies['frameworks/kwindowsystem'] = 'default'
        self.dependencies['frameworks/kxmlgui'] = 'default'
        self.dependencies['frameworks/kplotting'] = 'default'
        self.dependencies['frameworks/ktexteditor'] = 'default'
        self.dependencies['frameworks/kiconthemes'] = 'default'
        self.dependencies['win32libs/eigen3'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

