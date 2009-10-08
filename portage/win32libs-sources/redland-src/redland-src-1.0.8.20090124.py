import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        ver = '1.0.8'
        self.targets[ ver ] = 'http://download.librdf.org/source/redland-1.0.8.tar.gz'
        self.targetInstSrc[ ver ] = 'redland-1.0.8'
        self.patchToApply[ ver ] = ( 'redland-src_1.0.8.patch', 1 )
        self.defaultTarget = ver

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
        self.subinfo.options.package.packageName = 'redland'
        CMakePackageBase.__init__( self )
        
if __name__ == '__main__':
    Package().execute()
