import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = 'kf5 tier1'

    def setDependencies( self ):
        self.dependencies['frameworks/kauth'] = 'default'
        self.dependencies['frameworks/kcompletion'] = 'default'
        self.dependencies['frameworks/kcrash'] = 'default'
        self.dependencies['frameworks/kdnssd'] = 'default'
        self.dependencies['frameworks/kdoctools'] = 'default'
        self.dependencies['frameworks/kjobwidgets'] = 'default'
        self.dependencies['frameworks/kunitconversion'] = 'default'

from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        VirtualPackageBase.__init__( self )
