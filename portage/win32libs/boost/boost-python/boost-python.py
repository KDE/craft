import info
class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues("", tarballInstallSrc = self.package.replace("boost-","").replace("-", "_"))


        self.homepage = 'http://www.boost.org/'

        self.shortDescription = 'portable C++ libraries'


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['win32libs/boost-headers'] = 'default'
        self.buildDependencies['win32libs/boost-bjam'] = 'default'


from Package.BoostPackageBase import *

class Package( BoostPackageBase ):
    def __init__(self, **args):
        BoostPackageBase.__init__(self)


