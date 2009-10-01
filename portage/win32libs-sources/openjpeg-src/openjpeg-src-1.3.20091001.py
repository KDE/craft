import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '1.3' ] = 'http://openjpeg.googlecode.com/files/openjpeg_v1_3.tar.gz'
        self.targetInstSrc[ '1.3' ] = "openjpeg_v1_3"
        self.patchToApply[ '1.3' ] = ( 'openjpeg.diff', 1 )
        self.defaultTarget = '1.3'

    def setDependencies( self ):
        self.hardDependencies['win32libs-bin/tiff'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        self.subinfo.options.configure.defines = " -DBUILD_SHARED_LIBS=ON "
        CMakePackageBase.__init__( self )
        
if __name__ == '__main__':
    Package().execute()
