import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets( self ):
        ver = '0.1'
        self.targets[ ver ] = 'http://downloads.sourceforge.net/sourceforge/oscaf/shared-desktop-ontologies-0.1.tar.bz2'
        self.targetInstSrc[ ver ] = 'shared-desktop-ontologies-0.1'
        self.defaultTarget = ver

    def setDependencies( self ):
#        self.hardDependencies['win32libs-bin/pcre'] = 'default'
        pass


class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        
if __name__ == '__main__':
    Package().execute()
