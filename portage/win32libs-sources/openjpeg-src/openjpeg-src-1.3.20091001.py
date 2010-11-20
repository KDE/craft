import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '1.3' ] = 'http://openjpeg.googlecode.com/files/openjpeg_v1_3.tar.gz'
        self.targetInstSrc[ '1.3' ] = "openjpeg_v1_3"
        self.patchToApply[ '1.3' ] = ( 'openjpeg.diff', 1 )
        self.targetDigests['1.3'] = '8d6870d9500ea09e0b1d30b981bea1c8de534de4'
        self.svnTargets['svnHEAD'] = 'http://openjpeg.googlecode.com/svn/trunk/'
        self.options.configure.defines = " -DBUILD_SHARED_LIBS=ON "
        self.defaultTarget = '1.3'

    def setDependencies( self ):
        self.dependencies['win32libs-bin/tiff'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        
if __name__ == '__main__':
    Package().execute()
