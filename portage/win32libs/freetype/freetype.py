import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['2.3.12', '2.5.0.1']:
            self.targets[ver] = "http://downloads.sourceforge.net/freetype/freetype-" + ver + ".tar.bz2"
            self.targetInstSrc[ver] = "freetype-" + ver
        self.patchToApply['2.3.12'] = ('freetype-2.3.12.diff', 1)
        self.patchToApply['2.5.0.1'] = ('freetype-2.5.0.1.diff', 1)
        self.targetDigests['2.3.12'] = 'ebf0438429c0bedd310059326d91646c3c91016b'
        self.targetDigests['2.5.0.1'] = '4bbd8357b4b723e1ff38414a9eaf50bf99dacb84'

        self.defaultTarget = '2.5.0.1'
        self.shortDescription = "A Free, High-Quality, and Portable Font Engine"

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *
class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
  Package().execute()
