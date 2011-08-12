import info
import emergePlatform

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['2.0.4']:
            self.targets[ ver ] = 'http://download.librdf.org/source/raptor2-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'raptor2-' + ver
        self.patchToApply[ '2.0.4' ] = ( 'raptor2-2.0.4-20110811.diff', 1 )
        self.targetDigests['2.0.4'] = '79e1289f480cb0fe75f49ec29d9f49189a8a58c2'
        self.shortDescription = "Resource Description Framework (RDF)"
        self.defaultTarget = '2.0.4'

    def setDependencies( self ):
        self.dependencies['win32libs-bin/yajl'] = 'default'
        self.dependencies['win32libs-bin/expat'] = 'default'
        self.dependencies['win32libs-bin/libcurl'] = 'default'
        self.dependencies['win32libs-bin/libxml2'] = 'default'
        self.dependencies['win32libs-bin/libxslt'] = 'default'
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
