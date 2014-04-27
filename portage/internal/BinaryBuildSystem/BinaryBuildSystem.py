import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        return True

from Package.InternalPackageBase import *

class Package(InternalPackageBase):
    def __init__( self ):
        InternalPackageBase.__init__(self)

