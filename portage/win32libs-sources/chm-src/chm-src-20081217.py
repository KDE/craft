import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.40'] = 'http://www.jedrea.com/chmlib/chmlib-0.40.tar.bz2'
        self.patchToApply['0.40'] = ('chm-cmake.diff', 0)
        self.targetInstSrc['0.40'] = 'chmlib-0.40'
        self.targetDigests['0.40'] = '5231d7531e8808420d7f89fd1e4fdbac1ed7a167'
        self.defaultTarget = '0.40'
    
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

        # building examples and debugging tools
        self.subinfo.options.configure.defines = "-DBUILD_examples=OFF"

if __name__ == '__main__':
    Package().execute()
