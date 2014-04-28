import info
class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultVersions("http://downloads.sourceforge.net/boost/boost_${VERSION}.7z",
                                            tarballInstallSrc = "boost_${VERSION}")

        self.targetDigests['1_48_0'] = 'f221f067620e5af137e415869bd96ad667db9830'
        self.targetDigests['1_49_0'] = '406903ce4f946f44b126d6c8bfefafed2fc9fdc4'
        self.targetDigests['1_52_0'] = 'c3b2ef5633d4a6c30fece86ed9116be853695f82'
        self.targetDigests['1_54_0'] = '1a4b4b32aba8c396c0b661b03708d00c08f1c758'
        self.targetDigests['1_55_0'] = '09203c60118442561d0ee196772058d80226762d'

        self.patchToApply['1.48.0'] = [('boost_1_47_0-20110815.diff',1)]
        self.patchToApply['1_47_0'] = [('boost_1_47_0-20110815.diff',1)]
        self.patchToApply['1_49_0'] = [('boost_1_47_0-20110815.diff',1)]
        self.patchToApply['1_54_0'] = [('boost_1_54_0-spirit-20131114.diff',1)] # TODO: also include in future releases!
        self.patchToApply['1_55_0'] = [('boost_1_54_0-spirit-20131114.diff',1)] # TODO: also include in future releases!

        self.homepage = 'http://www.boost.org/'

        self.shortDescription = 'portable C++ libraries'


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'


from Package.BoostPackageBase import *
class Package(BoostPackageBase):
    def __init__(self, **args):
        BoostPackageBase.__init__(self)

    def make(self):
        return True

    def install(self):
        shutil.copytree(os.path.join(self.sourceDir(), 'boost'),
                        os.path.join(self.imageDir(), 'include' , 'boost'))        #disable autolinking
        f = open(os.path.join(self.imageDir(),'include', 'boost', 'config', 'user.hpp'), 'a')
        f.write('#define BOOST_ALL_NO_LIB\n')
        f.close()
        return True


