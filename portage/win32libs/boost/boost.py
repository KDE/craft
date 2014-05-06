import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.versionInfo.setDefaultValues("")

        self.homepage = 'http://www.boost.org/'

        self.shortDescription = 'portable C++ libraries'

    def setDependencies( self ):
        self.dependencies['win32libs/boost-headers'] = 'default'
        self.dependencies['win32libs/boost-bjam'] = 'default'
        self.dependencies['win32libs/boost-graph'] = 'default'
        self.dependencies['win32libs/boost-program-options'] = 'default'
        if self.options.features.pythonSupport:
            self.dependencies['win32libs/boost-python'] = 'default'
        self.dependencies['win32libs/boost-regex'] = 'default'
        self.dependencies['win32libs/boost-system'] = 'default'
        self.dependencies['win32libs/boost-thread'] = 'default'
        self.dependencies['win32libs/boost-random'] = 'default'

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        VirtualPackageBase.__init__( self )


