import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = ''
        self.defaultTarget = 'gitHEAD'
        self.shortDescription = 'kf5 tier1'

    def setDependencies( self ):
        self.dependencies['frameworks/attica'] = 'default'
        self.dependencies['frameworks/karchive'] = 'default'
        self.dependencies['frameworks/kcodecs'] = 'default'
        self.dependencies['frameworks/kconfig'] = 'default'
        self.dependencies['frameworks/kcoreaddons'] = 'default'
        self.dependencies['frameworks/kdbusaddons'] = 'default'
        self.dependencies['frameworks/kglobalaccel'] = 'default'
        self.dependencies['frameworks/kguiaddons'] = 'default'
        self.dependencies['frameworks/ki18n'] = 'default'
        self.dependencies['frameworks/kidletime'] = 'default'
        self.dependencies['frameworks/kimageformats'] = 'default'
        self.dependencies['frameworks/kitemmodels'] = 'default'
        self.dependencies['frameworks/kitemviews'] = 'default'
        self.dependencies['frameworks/kjs'] = 'default'
        self.dependencies['frameworks/kplotting'] = 'default'
        self.dependencies['frameworks/kwidgetsaddons'] = 'default'
        self.dependencies['frameworks/kwindowsystem'] = 'default'
        self.dependencies['frameworks/solid'] = 'default'
        self.dependencies['frameworks/sonnet'] = 'default'
        self.dependencies['frameworks/threadweaver'] = 'default'


from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        VirtualPackageBase.__init__( self )

