import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = 'kf5 tier1'

    def setDependencies( self ):
        self.dependencies['kde/kbookmarks'] = 'default'
        self.dependencies['kde/kconfigwidgets'] = 'default'
        self.dependencies['kde/kiconthemes'] = 'default'
        self.dependencies['kde/kio'] = 'default'
        self.dependencies['kde/knotifications'] = 'default'
        self.dependencies['kde/kparts'] = 'default'
        self.dependencies['kde/kservice'] = 'default'
        self.dependencies['kde/ktextwidgets'] = 'default'
        self.dependencies['kde/kwallet'] = 'default'
        self.dependencies['kde/kxmlgui'] = 'default'
        


from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        VirtualPackageBase.__init__( self )

