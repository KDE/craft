import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = 'kf5 tier1'

    def setDependencies( self ):
        self.dependencies['kde/attica'] = 'default'
        self.dependencies['kde/karchive'] = 'default'
        self.dependencies['kde/kcodecs'] = 'default'
        self.dependencies['kde/kconfig'] = 'default'
        self.dependencies['frameworks/kcoreaddons'] = 'default'
        self.dependencies['kde/kdbusaddons'] = 'default'
        self.dependencies['kde/kglobalaccel'] = 'default'
        self.dependencies['kde/kguiaddons'] = 'default'
        self.dependencies['kde/ki18n'] = 'default'
        self.dependencies['kde/kidletime'] = 'default'
        self.dependencies['kde/kimageformats'] = 'default'
        self.dependencies['kde/kitemmodels'] = 'default'
        self.dependencies['kde/kitemviews'] = 'default'
        self.dependencies['kde/kjs'] = 'default'
        self.dependencies['kde/kplotting'] = 'default'
        self.dependencies['frameworks/kwidgetsaddons'] = 'default'
        self.dependencies['kde/kwindowsystem'] = 'default'
        self.dependencies['kde/solid'] = 'default'
        self.dependencies['kde/sonnet'] = 'default'
        self.dependencies['kde/threadweaver'] = 'default'


from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        VirtualPackageBase.__init__( self )

