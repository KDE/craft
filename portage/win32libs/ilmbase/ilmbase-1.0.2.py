import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '1.0' ] = 'http://download.savannah.gnu.org/releases/openexr/ilmbase-1.0.2.tar.gz'
        self.targetInstSrc[ '1.0' ] = "ilmbase-1.0.2"
        self.patchToApply[ '1.0' ] = [( 'ilmbase-1.0.2-20120804.diff', 1 )]
        self.targetDigests['1.0'] = 'fe6a910a90cde80137153e25e175e2b211beda36'
        #self.options.configure.defines = " -DBUILD_SHARED_LIBS=ON "
        self.shortDescription = "a library for handling half (16 bit float)"
        self.defaultTarget = '1.0'

#    def setDependencies( self ):
#        self.dependencies['win32libs/tiff'] = 'default'

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
