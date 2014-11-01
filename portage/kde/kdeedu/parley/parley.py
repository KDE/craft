import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:%s|%s|' % (self.package, "frameworks")

        self.shortDescription = 'a vocabulary trainer'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtsvg'] = 'default'
        self.buildDependencies['frameworks/kdoctools'] = 'default'
        self.dependencies['frameworks/kcoreaddons'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kcrash'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['frameworks/kio'] = 'default'
        self.dependencies['frameworks/knewstuff'] = 'default'
        #self.dependencies['frameworks/kross'] = 'default'
        self.dependencies['frameworks/khtml'] = 'default'
        self.dependencies['frameworks/sonnet'] = 'default'
        self.dependencies['frameworks/kcmutils'] = 'default'
        self.dependencies['frameworks/kxmlgui'] = 'default'
        self.dependencies['frameworks/knotifications'] = 'default'
        self.dependencies['kde/libkeduvocdocument'] = 'default'
        self.dependencies['win32libs/libxslt'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

