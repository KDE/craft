import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:k3b'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdemultimedia'] = 'default'
        self.dependencies['win32libs/libsamplerate'] = 'default'
        self.dependencies['testing/libdvdcss'] = 'default'
        #        self.dependencies['testing/libcdio'] = 'default'

class Package(CMakePackageBase):
    def __init__( self):
        CMakePackageBase.__init__(self)

