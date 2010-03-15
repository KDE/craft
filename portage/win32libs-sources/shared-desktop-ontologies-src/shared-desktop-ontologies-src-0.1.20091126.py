import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['0.1', '0.2','0.3']:
            self.targets[ ver ] = 'http://downloads.sourceforge.net/sourceforge/oscaf/shared-desktop-ontologies-' + ver + '.tar.bz2'
            self.targetInstSrc[ ver ] = 'shared-desktop-ontologies-' + ver
        self.options.package.withCompiler = False
        self.defaultTarget = '0.3'

    def setDependencies( self ):
        pass


class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        
if __name__ == '__main__':
    Package().execute()
