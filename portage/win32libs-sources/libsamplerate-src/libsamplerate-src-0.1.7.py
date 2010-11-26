import info

from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['0.1.7'] = "http://www.mega-nerd.com/SRC/libsamplerate-0.1.7.tar.gz"
        self.targetInstSrc['0.1.7'] = 'libsamplerate-0.1.7'
        self.targetDigests['0.1.7'] = '98a52392eb97f9ba724ca024b3af29a8a0cc0206'
        self.patchToApply['0.1.7'] = ('libsamplerate-0.1.7-20091002.diff', 1)
        self.defaultTarget = '0.1.7'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/libsndfile'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        self.subinfo.options.configure.defines = " -DBUILD_SHARED_LIB=ON -DBUILD_EXAMPLES=ON -DBUILD_TESTS=ON"
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
