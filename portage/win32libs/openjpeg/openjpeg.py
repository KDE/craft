import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '1.3' ] = 'http://openjpeg.googlecode.com/files/openjpeg_v1_3.tar.gz'
        for ver in ['1.5.1', '2.0.0']:
            self.targets[ ver ] = 'http://openjpeg.googlecode.com/files/openjpeg-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = "openjpeg-" + ver
        self.targetInstSrc[ '1.3' ] = "openjpeg_v1_3"
        self.patchToApply[ '1.3' ] = ( 'openjpeg.diff', 1 )
        self.targetDigests['1.3'] = '8d6870d9500ea09e0b1d30b981bea1c8de534de4'
        self.targetDigests['1.5.1'] = '1b0b74d1af4c297fd82806a9325bb544caf9bb8b'
        self.targetDigests['2.0.0'] = '0af78ab2283b43421458f80373422d8029a9f7a7'
        self.svnTargets['svnHEAD'] = 'http://openjpeg.googlecode.com/svn/trunk/'
        self.options.configure.defines = " -DBUILD_SHARED_LIBS=ON -DOPENJPEG_INSTALL_INCLUDE_DIR=\"include/openjpeg\""
        self.shortDescription = "a library for handling JPEG2000 image formats"
        self.defaultTarget = '1.5.1'

    def setDependencies( self ):
        self.dependencies['win32libs/tiff'] = 'default'
        self.dependencies['win32libs/libpng'] = 'default'
        self.dependencies['win32libs/lcms2'] = 'default'
        self.dependencies['win32libs/zlib'] = 'default'

class Package(CMakePackageBase):
    def __init__( self ):
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
