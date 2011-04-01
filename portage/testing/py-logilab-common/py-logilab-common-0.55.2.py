import base
import utils
import os
import sys
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.55.2'] = 'http://ftp.logilab.org/pub/common/logilab-common-0.55.2.tar.gz'
        self.targetInstSrc['0.55.2'] = 'logilab-common-0.55.2'
        self.targetDigests['0.55.2'] = 'dd0123ccf0d69c1e52449906817abdb2e91655a4'
        self.defaultTarget = '0.55.2'

from Package.PythonPackageBase import *
        
class Package(PythonPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        PythonPackageBase.__init__( self )
        
if __name__ == '__main__':
    Package().execute()
