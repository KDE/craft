import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        for v in [ '2.7.0', '2.8.4' ]:
            self.targets[ v ] = 'http://libarchive.googlecode.com/files/libarchive-' + v + '.tar.gz'
            self.targetInstSrc[ v ] = 'libarchive-' + v
        self.targetDigests['2.8.4'] = 'b9cc3bbd20bd71f996be9ec738f19fda8653f7af'
        self.shortDescription = "C library and command-line tools for reading and writing tar, cpio, zip, ISO, and other archive formats"
        self.defaultTarget = '2.8.4'
    
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs-bin/libbzip2'] = 'default'
#        self.dependencies['win32libs-bin/lzma'] = 'default'
        self.dependencies['win32libs-bin/openssl'] = 'default'
        self.dependencies['win32libs-bin/zlib'] = 'default'

from Package.CMakePackageBase import *
        
class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
