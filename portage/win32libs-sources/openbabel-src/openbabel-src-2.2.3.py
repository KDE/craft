import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.2.0'] = 'http://downloads.sourceforge.net/sourceforge/openbabel/openbabel-2.2.0.tar.gz'
        self.targets['2.2.3'] = 'http://downloads.sourceforge.net/sourceforge/openbabel/openbabel-2.2.3.tar.gz'
        self.patchToApply['2.2.0'] = ('openbabel-2.2.0-cmake.diff', 0)
        self.targetInstSrc['2.2.0'] = 'openbabel-2.2.0'
        self.targetInstSrc['2.2.3'] = 'openbabel-2.2.3'
        self.shortDescription = "library to convert the various file formats used in chemical software"
        self.defaultTarget = '2.2.3'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.buildDependencies['win32libs-bin/boost'] = 'default'
        self.dependencies['win32libs-bin/zlib'] = 'default'
        self.dependencies['win32libs-bin/libxml2'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
