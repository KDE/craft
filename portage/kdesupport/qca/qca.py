import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['libs/qtbase'] = 'default'
        self.dependencies['win32libs/openssl'] = 'default'
        self.dependencies['win32libs/cyrus-sasl'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'kde:qca.git|qt5'
        self.shortDescription = "Qt Cryptographic Architecture (QCA)"
        self.defaultTarget = 'gitHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__(self)



