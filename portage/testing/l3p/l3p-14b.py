import base
import os
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets[ '14b' ] =  "http://www.hassings.dk/l3/l3p/l3p14beta.zip"
        self.targetDigests['14b'] = '616e563e07a57ff48d1d8b9305cf45ed3f585d83'
        self.shortDescription = 'a ready-to-render POV-Ray-file from any LDRAW model converter'
        self.defaultTarget = '14b'

    def setDependencies( self ):
        self.buildDependencies['virtual/bin-base'] = 'default'

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        BinaryPackageBase.__init__( self )
        self.subinfo.options.install.installPath = "bin"

if __name__ == '__main__':
    Package().execute()
