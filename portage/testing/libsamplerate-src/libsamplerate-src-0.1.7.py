import info

from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['0.1.7'] = "http://www.mega-nerd.com/SRC/libsamplerate-0.1.7.tar.gz"
        self.targetDigests['0.1.7'] = 'f3f803ec5feae5a3fdb0fa3937277669e854386e'
        self.targetInstSrc['0.1.7'] = 'libsamplerate-0.1.7'
        self.patchToApply['0.1.7'] = ('libsamplerate-0.1.7-20091002.diff', 1)
        self.options.package.withCompiler = False
        self.options.package.packageName = "libsamplerate"
        self.defaultTarget = '0.1.7'
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        self.subinfo.options.configure.defines = " -DBUILD_SHARED_LIB=ON -DBUILD_EXAMPLES=ON -DBUILD_TESTS=ON"
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
