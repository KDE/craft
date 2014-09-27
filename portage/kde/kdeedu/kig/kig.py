import info
import kdedefaults as kd
from EmergeConfig import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['frameworks'] = '[git]kde:kig|frameworks'

        self.shortDescription = 'interactive geometry'
        self.defaultTarget = 'frameworks'

    def setDependencies( self ):
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['libs/qtsvg'] = 'default'
        self.dependencies['kde/kparts'] = 'default'
        self.dependencies['kde/kdoctools'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['kde/ktexteditor'] = 'default'
        self.dependencies['kde/kiconthemes'] = 'default'
        self.dependencies['frameworks/kconfigwidgets'] = 'default'
        self.dependencies['frameworks/karchive'] = 'default'
        self.dependencies['kde/kdelibs4support'] = 'default'
        # only needed for unit tests
        self.buildDependencies['kde/kemoticons'] = 'default'
        self.buildDependencies['frameworks/kitemmodels'] = 'default'
        if self.options.features.pythonSupport:
            self.dependencies['win32libs/boost-python'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

