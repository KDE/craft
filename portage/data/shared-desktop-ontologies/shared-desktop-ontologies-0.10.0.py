import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['0.1', '0.2','0.3', '0.4', '0.5','0.5-1','0.6.0','0.7.0', '0.7.1', '0.9.0', '0.10.0']:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/sourceforge/oscaf/shared-desktop-ontologies-' + ver + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'shared-desktop-ontologies-' + ver
        self.targetDigests['0.4'] = '7ca3522dd9d58329966f46a3b18fa57b0b2280a8'
        self.targetDigests['0.5'] = '672e10ba113314083b43702d9456a9c92e4f501f'
        self.targetDigests['0.5-1'] = '672e10ba113314083b43702d9456a9c92e4f501f'
        self.patchToApply['0.5-1'] = ('shared-desktop-ontologies-0.5-20101125.diff', 1)
        self.targetDigests['0.7.0'] = '2e4dd2ecd24c5f0432b3a4263aeddff74663f266'
        self.targetDigests['0.7.1'] = '14c6998effdfe880ec8adbdf47fe010f62af4037'
        self.targetDigests['0.9.0'] = 'c5dffbc58a5a694a36f7da4f7806e37cab459722'
        self.targetDigests['0.10.0'] = 'cfa3dee770ca979aea0362064c0ba5c5df3f8c9b'

        # A syntax problem with raptor 2.0.4
        self.patchToApply['0.7.1'] = ('shared-desktop-ontologies-0.7.1-20110811.diff', 1)
        self.patchToApply['0.9.0'] = ('shared-desktop-ontologies-0.7.1-20110811.diff', 1)
        self.patchToApply['0.10.0'] = ('shared-desktop-ontologies-0.7.1-20110811.diff', 1)
        
        self.shortDescription = "the core ontologies such as RDF or RDFS and all Nepomuk ontologies"
        self.options.package.withCompiler = False
        self.defaultTarget = '0.10.0'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
