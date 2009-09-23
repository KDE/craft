import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '1.0.8-1' ] = 'http://download.librdf.org/source/redland-1.0.8.tar.gz'
        self.targetInstSrc[ '1.0.8-1' ] = 'redland-1.0.8'
        self.patchToApply[ '1.0.8-1' ] = ( 'redland-src_1.0.8.patch', 1 )
        self.defaultTarget = '1.0.8-1'

    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/sqlite'] = 'default'
        self.hardDependencies['win32libs-bin/libcurl'] = 'default'
        self.hardDependencies['win32libs-bin/libxml2'] = 'default'
        self.hardDependencies['win32libs-bin/libxslt'] = 'default'
        self.hardDependencies['win32libs-bin/openssl'] = 'default'
        self.hardDependencies['win32libs-bin/pcre'] = 'default'


class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        
if __name__ == '__main__':
    Package().execute()
