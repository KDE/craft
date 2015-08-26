import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = "KDE Networking applications (Kopete, KGet)"

    def setDependencies( self ):
#        self.dependencies['kde/kdenetwork-filesharing'] = 'default'
        self.dependencies['kde/kdenetwork-strigi-analyzers'] = 'default'
        self.dependencies['frameworks/kdnssd'] = 'default' # this builds fine, but is it really useful?
        self.dependencies['kde/kget'] = 'default'
        self.dependencies['kde/kopete'] = 'default'
#        self.dependencies['kde/kppp'] = 'default' # doesn't build on windows
        self.dependencies['kde/krdc'] = 'default' # this builds fine, but is it really useful?
#        self.dependencies['kde/krfb'] = 'default' # doesn't build on windows

from Package.VirtualPackageBase import *

class Package(VirtualPackageBase):
    def __init__( self ):
        VirtualPackageBase.__init__( self )

