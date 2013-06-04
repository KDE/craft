import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.50.0', '1.52.0']:
            self.svnTargets[ver] = ''
        self.defaultTarget = '1.52.0'

        self.homepage = 'http://www.boost.org/'

        self.shortDescription = 'portable C++ libraries'

    def setDependencies( self ):
        self.dependencies['win32libs/boost-headers'] = 'default'
        self.dependencies['win32libs/boost-bjam'] = 'default'
        self.dependencies['win32libs/boost-graph'] = 'default'
        self.dependencies['win32libs/boost-program-options'] = 'default'
        self.dependencies['win32libs/boost-python'] = 'default'
        self.dependencies['win32libs/boost-regex'] = 'default'
        self.dependencies['win32libs/boost-system'] = 'default'
        self.dependencies['win32libs/boost-thread'] = 'default'

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
