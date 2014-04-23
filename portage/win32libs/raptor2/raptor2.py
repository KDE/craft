import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['2.0.4', '2.0.8']:
            self.targets[ ver ] = 'http://download.librdf.org/source/raptor2-' + ver + '.tar.gz'
            self.targetInstSrc[ ver ] = 'raptor2-' + ver
        self.patchToApply[ '2.0.4' ] = [( 'raptor2-2.0.4-20110811.diff', 1 ),
                                        ( 'raptor2_lround_and_isnan_patch.diff', 1)
                                       ]
        self.patchToApply[ '2.0.8' ] = [( 'raptor2-2.0.8-20130522.diff', 1 )
                                       ]
        self.targetDigests['2.0.4'] = '79e1289f480cb0fe75f49ec29d9f49189a8a58c2'
        self.targetDigests['2.0.8'] = '6caec62d28dbf5bc26e8de5a46101b52aabf94fd'
        self.shortDescription = "Resource Description Framework (RDF)"
        self.svnTargets['gitHEAD'] = 'git://github.com/dajobe/raptor.git'
        self.defaultTarget = '2.0.8'

    def setDependencies( self ):
        self.dependencies['win32libs/yajl'] = 'default'
        self.dependencies['win32libs/expat'] = 'default'
        self.dependencies['win32libs/libcurl'] = 'default'
        self.dependencies['win32libs/libxml2'] = 'default'
        self.dependencies['win32libs/libxslt'] = 'default'
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
