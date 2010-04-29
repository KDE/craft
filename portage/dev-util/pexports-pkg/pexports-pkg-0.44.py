import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.44'] = 'http://tml.pp.fi/pexports-0.44.zip'
        self.targetInstSrc['0.44'] = 'pexports-0.44'  # this only helps for building
        self.patchToApply['0.44'] = ('pexports-0.44-20100421.diff', 1)
        self.targetDigests['0.44'] = 'd40111ba34330dbbcea459d3b915f3406f840807'
        self.defaultTarget = '0.44'

    def setDependencies( self ):
        self.hardDependencies['gnuwin32/bison'] = 'default'
        self.hardDependencies['gnuwin32/flex'] = 'default'
        
        
from Package.CMakePackageBase import *        
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = 'dev-utils'
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.unpack.unpackDir = 'pexports-0.44'
        self.subinfo.options.package.packageName = 'pexports'
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()


