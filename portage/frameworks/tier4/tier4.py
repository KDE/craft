import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'
        self.shortDescription = 'kf5 tier4'

    def setDependencies( self ):
        self.dependencies['frameworks/kdelibs4support'] = 'default'
        self.dependencies['frameworks/frameworkintegration'] = 'default'
        self.dependencies['frameworks/libkdcraw'] = 'default'


from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        VirtualPackageBase.__init__( self )
