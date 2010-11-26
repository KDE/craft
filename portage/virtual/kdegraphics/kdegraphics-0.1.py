from Package.VirtualPackageBase import *
import info
import os

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets[ '0.1' ] = ""
        self.defaultTarget = '0.1'
    
    def setDependencies( self ):
        if os.getenv( "EMERGE_DEFAULTCATEGORY" ) in [ 'kde-4.4', 'kde-4.5', 'kde-4.6' ]:
            self.dependencies[ os.getenv( "EMERGE_DEFAULTCATEGORY" ) + '/kdegraphics' ]  = 'default'
        else:
            self.dependencies[ 'kde/kdegraphics' ]  = 'default'
    
class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
