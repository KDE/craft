import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues( )
        self.shortDescription = "All kind of addons to improve your Plasma experience"

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kde-workspace'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['kde/marble'] = 'default'
        self.dependencies['kde/libkexiv2'] = 'default'
        self.dependencies['kdesupport/attica'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['kdesupport/qjson'] = 'default'
        self.dependencies['kdesupport/dbusmenu-qt'] = 'default'
        self.dependencies['win32libs/eigen2'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

