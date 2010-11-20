import base
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for v in [ '2.7.0' ]:
            self.targets[ v ] = 'http://libarchive.googlecode.com/files/libarchive-' + v + '.tar.gz'
            self.targetInstSrc[ v ] = 'libarchive-' + v
        self.defaultTarget = '2.7.0'
    
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/libbzip2'] = 'default'
#        self.dependencies['win32libs-bin/lzma'] = 'default'
        self.dependencies['win32libs-bin/openssl'] = 'default'
        self.dependencies['win32libs-bin/zlib'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
