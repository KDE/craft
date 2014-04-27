import info
class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.44.0', '1.47.0', '1.48.0', '1.49.0', '1.50.0', '1.52.0', '1.54.0','1.55.0']:
            self.targets[ver] = ''
            self.targetInstSrc[ver] = 'graph'.replace('-','_')
        self.defaultTarget = '1.55.0'


        self.homepage = 'http://www.boost.org/'

        self.shortDescription = 'portable C++ libraries'


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['win32libs/boost-headers'] = 'default'
        self.buildDependencies['win32libs/boost-bjam'] = 'default'
        self.dependencies['win32libs/boost-regex'] = 'default'


from Package.BoostPackageBase import *

class Package( BoostPackageBase ):
    def __init__(self, **args):
        BoostPackageBase.__init__(self)


