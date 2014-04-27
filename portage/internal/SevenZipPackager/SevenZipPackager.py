import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['dev-util/7zip'] = 'default'

from Package.InternalPackageBase import *

class Package(InternalPackageBase):
    def __init__( self ):
        InternalPackageBase.__init__(self)

