import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.23.0'] = 'http://ftp.logilab.org/pub/pylint/pylint-0.23.0.tar.gz'
        self.targetInstSrc['0.23.0'] = 'pylint-0.23.0'
        self.targetDigests['0.23.0'] = 'd06e759693df4619233b8d386201f463be4a3663'
        self.defaultTarget = '0.23.0'
        
    def setDependencies( self ):
        self.hardDependencies['testing/py-logilab-astng'] = 'default'
        self.hardDependencies['testing/py-logilab-common'] = 'default'
        
from Package.PythonPackageBase import *
        
class Package(PythonPackageBase):
    def __init__( self ):
        PythonPackageBase.__init__( self )

