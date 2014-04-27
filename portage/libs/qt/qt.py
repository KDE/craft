import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['libs/qt5'] = 'default'
        
        
        

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        VirtualPackageBase.__init__( self )


