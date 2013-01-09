import info
import emergePlatform

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['1.0.14']:
            self.targets[ ver ] = 'http://download.librdf.org/source/redland-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'redland-' + ver
        self.patchToApply[ '1.0.14' ] = [( 'redland-1.0.14-20110811.diff', 1 )]
        self.targetDigests['1.0.14'] = '2561bf73f00f88e39f5c7b3a9b78f8d4ce7da955'
        self.shortDescription = "Resource Description Framework (RDF)"
        self.defaultTarget = '1.0.14'

    def setDependencies( self ):
        self.dependencies['win32libs/raptor2'] = 'default'
        self.dependencies['win32libs/rasqal'] = 'default'
        self.dependencies['win32libs/sqlite'] = 'default'
        self.dependencies['win32libs/pthreads'] = 'default'
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
