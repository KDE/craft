import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ '3.5.21', '3.5.23', '3.5.25.3' ]:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/djvu/djvulibre-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'djvulibre-' + ver
        self.targetInstSrc['3.5.25.3'] = 'djvulibre-3.5.25'
        self.patchToApply[ '3.5.21' ] = ( "djvu-cmake.diff", 0 )
        self.patchToApply[ '3.5.23' ] = ( "djvulibre-3.5.23-20101116.diff", 1 )
        self.patchToApply[ '3.5.25.3' ] = ( "djvulibre-3.5.25.3-20130906.diff", 1 )
        self.targetDigests['3.5.23'] = 'b19f6b461515a52eb1048aec81e04dfd836d681f'
        self.targetDigests['3.5.25.3'] = 'ad35056aabb1950f385360ff59520a82a6f779ec'

        self.shortDescription = "DjVuLibre is an implementation of DjVu image file format"
        self.defaultTarget = '3.5.25.3'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
