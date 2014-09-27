import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['frameworks'] = '[git]kde:kanagram|master'

        self.shortDescription = 'a letter order game'
        self.defaultTarget = 'frameworks'

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtdeclarative'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['frameworks/kcrash'] = 'default'
        self.dependencies['frameworks/sonnet'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kconfigwidgets'] = 'default'
        self.dependencies['frameworks/kdeclarative'] = 'default'
        self.dependencies['frameworks/kio'] = 'default'
        self.dependencies['frameworks/knewstuff'] = 'default'
        self.dependencies['kde/kdelibs4support'] = 'default'
        self.dependencies['kde/libkeduvocdocument'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

