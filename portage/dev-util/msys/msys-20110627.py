import info
import compiler


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ "20110627" ] = ""


    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        self.dependencies['dev-util/minsys'] = 'default'
        if compiler.isMinGW():
            self.dependencies['dev-util/libtool'] = 'default'
            self.dependencies['dev-util/autotools'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = False
        self.disableTargetBuild = True

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )


if __name__ == '__main__':
    Package().execute()
