import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['0.1', '0.2','0.3', '0.4', '0.5']:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/sourceforge/oscaf/shared-desktop-ontologies-' + ver + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'shared-desktop-ontologies-' + ver
        self.targets[ '0.5-1' ] = 'http://downloads.sourceforge.net/sourceforge/oscaf/shared-desktop-ontologies-' + '0.5' + '.tar.bz2'
        self.targetInstSrc[ '0.5-1' ] = 'shared-desktop-ontologies-' + '0.5'
        self.targetDigests['0.4'] = '7ca3522dd9d58329966f46a3b18fa57b0b2280a8'
        self.targetDigests['0.5'] = '672e10ba113314083b43702d9456a9c92e4f501f'
        self.targetDigests['0.5-1'] = '672e10ba113314083b43702d9456a9c92e4f501f'
        self.patchToApply['0.5-1'] = ('shared-desktop-ontologies-0.5-20101125.diff', 1)
        self.defaultTarget = '0.5'

    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        
if __name__ == '__main__':
    Package().execute()
