import info


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets[ "gitHEAD" ] = "https://github.com/phacility/libphutil.git"
        self.targetInstallPath[ "gitHEAD" ] = "dev-utils/arcanist/libphutil"
        self.defaultTarget = "gitHEAD"



    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'
        self.buildDependencies['binary/php'] = 'default'


from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        BinaryPackageBase.__init__(self)

    def unpack(self):
        return True
    
