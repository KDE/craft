import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = 'kf5 tier1'

    def setDependencies( self ):
        self.dependencies['kde/kauth'] = 'default'
        self.dependencies['kde/kcompletion'] = 'default'
        self.dependencies['kde/kcrash'] = 'default'
        self.dependencies['kde/kdnssd'] = 'default'
        self.dependencies['kde/kdoctools'] = 'default'
        self.dependencies['kde/kjobwidgets'] = 'default'
        self.dependencies['kde/kunitconversion'] = 'default'

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        VirtualPackageBase.__init__( self )
