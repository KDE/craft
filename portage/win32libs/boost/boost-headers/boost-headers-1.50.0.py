import info
class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.44.0', '1.47.0', '1.48.0', '1.49.0', '1.50.0', '1.52.0']:
            verString = ver.replace('.','_')
            self.targets[ver] = 'http://downloads.sourceforge.net/boost/boost_%s.7z' % verString
            self.targetInstSrc[ver] = 'boost_%s' % verString

        self.defaultTarget = '1.52.0'

        self.targetDigests['1.48.0'] = 'f221f067620e5af137e415869bd96ad667db9830'
        self.targetDigests['1.49.0'] = '406903ce4f946f44b126d6c8bfefafed2fc9fdc4'
        self.targetDigests['1.52.0'] = 'c3b2ef5633d4a6c30fece86ed9116be853695f82'

        self.patchToApply['1.48.0'] = [('boost_1_47_0-20110815.diff',1)]
        self.patchToApply['1.47.0'] = [('boost_1_47_0-20110815.diff',1)]
        self.patchToApply['1.49.0'] = [('boost_1_47_0-20110815.diff',1)]

        self.homepage = 'http://www.boost.org/'

        self.shortDescription = 'portable C++ libraries'


    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'


from Package.BoostPackageBase import *
class Package(BoostPackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
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


if __name__ == '__main__':
    Package().execute()
