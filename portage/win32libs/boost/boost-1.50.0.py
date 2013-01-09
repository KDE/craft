import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['1.50.0'] = ''
        self.defaultTarget = '1.50.0'

        self.homepage = 'http://www.boost.org/'

        self.shortDescription = 'portable C++ libraries'

    def setDependencies( self ):
        self.dependencies['win32libs/boost-headers-src'] = 'default'
        self.dependencies['win32libs/boost-bjam-src'] = 'default'
        self.dependencies['win32libs/boost-graph-src'] = 'default'
        self.dependencies['win32libs/boost-program-options-src'] = 'default'
        self.dependencies['win32libs/boost-python-src'] = 'default'
        self.dependencies['win32libs/boost-regex-src'] = 'default'
        self.dependencies['win32libs/boost-system-src'] = 'default'
        self.dependencies['win32libs/boost-thread-src'] = 'default'

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
