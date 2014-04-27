import info
import compiler


class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ "20110627" ] = ""


    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        if not self.options.features.msys2:
            self.dependencies['dev-util/minsys'] = 'default'
            if compiler.isMinGW():
                self.dependencies['dev-util/libtool'] = 'default'
                self.dependencies['dev-util/autotools'] = 'default'
        else:
            self.dependencies['dev-util/msys2'] = 'default'


from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        VirtualPackageBase.__init__( self )


