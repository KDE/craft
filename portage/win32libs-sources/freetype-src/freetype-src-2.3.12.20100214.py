import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.3.12'] = "http://downloads.sourceforge.net/freetype/freetype-2.3.12.tar.bz2"
        self.patchToApply['2.3.12'] = ('freetype-2.3.12.diff', 1)
        self.targetInstSrc['2.3.12'] = "freetype-2.3.12"
        self.defaultTarget = '2.3.12'
        self.targetDigests['2.3.12'] = 'ebf0438429c0bedd310059326d91646c3c91016b'
        self.shortDescription = "A Free, High-Quality, and Portable Font Engine"

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
  Package().execute()
