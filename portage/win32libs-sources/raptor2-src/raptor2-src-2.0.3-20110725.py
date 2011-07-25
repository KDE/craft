import info
import emergePlatform

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['2.0.3']:
            self.targets[ ver ] = 'http://download.librdf.org/source/raptor2-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'raptor2-' + ver
        self.patchToApply[ '2.0.3' ] = ( 'raptor2-2.0.3-20110726.diff', 1 )
        self.targetDigests['2.0.3'] = '996f532b059397f96a9b0cc231f6b2362f0b1184'
        self.shortDescription = "Resource Description Framework (RDF)"
        self.defaultTarget = '2.0.3'

    def setDependencies( self ):
        self.dependencies['testing/yajl-src'] = 'default'
        self.dependencies['win32libs-bin/expat'] = 'default'
        self.dependencies['win32libs-bin/libcurl'] = 'default'
        self.dependencies['win32libs-bin/libxml2'] = 'default'
        self.dependencies['win32libs-bin/libxslt'] = 'default'
        self.buildDependencies['virtual/base'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
