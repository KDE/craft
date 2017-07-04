import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['master'] = ''
        self.defaultTarget = 'master'
        self.shortDescription = 'kf5 tier1'

    def setDependencies( self ):
        self.runtimeDependencies['frameworks/attica'] = 'default'
        self.runtimeDependencies['frameworks/karchive'] = 'default'
        # kapidox doesn't work as we are not tied to a python interpreter / library
        #self.runtimeDependencies['frameworks/kapidox'] = 'default'
        self.runtimeDependencies['frameworks/kcodecs'] = 'default'
        self.runtimeDependencies['frameworks/kconfig'] = 'default'
        self.runtimeDependencies['frameworks/kcoreaddons'] = 'default'
        self.runtimeDependencies['frameworks/kdbusaddons'] = 'default'
        self.runtimeDependencies['frameworks/kguiaddons'] = 'default'
        self.runtimeDependencies['frameworks/ki18n'] = 'default'
        self.runtimeDependencies['frameworks/kidletime'] = 'default'
        self.runtimeDependencies['frameworks/kimageformats'] = 'default'
        self.runtimeDependencies['frameworks/kitemmodels'] = 'default'
        self.runtimeDependencies['frameworks/kitemviews'] = 'default'
        self.runtimeDependencies['frameworks/kplotting'] = 'default'
        self.runtimeDependencies['frameworks/kwidgetsaddons'] = 'default'
        self.runtimeDependencies['frameworks/kwindowsystem'] = 'default'
        self.runtimeDependencies['frameworks/solid'] = 'default'
        self.runtimeDependencies['frameworks/sonnet'] = 'default'
        self.runtimeDependencies['frameworks/threadweaver'] = 'default'
        self.runtimeDependencies['frameworks/breeze-icons'] = 'default'


from Package.VirtualPackageBase import *

class Package( VirtualPackageBase ):
    def __init__( self ):
        VirtualPackageBase.__init__( self )

