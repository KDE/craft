import info


class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in [ '3.5.21', '3.5.23' ]:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/djvu/djvulibre-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'djvulibre-' + ver
        self.patchToApply[ '3.5.21' ] = ( "djvu-cmake.diff", 0 )
        self.patchToApply[ '3.5.23' ] = ( "djvulibre-3.5.23-20101116.diff", 1 )
        self.targetDigests['3.5.23'] = 'b19f6b461515a52eb1048aec81e04dfd836d681f'
        self.defaultTarget = '3.5.23'
    
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
