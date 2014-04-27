import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['5.4.2'] = 'http://www.xs4all.nl/~mlaan2/ispack/ispack-5.4.2.exe'
        self.defaultTarget = '5.4.2'

from Package.SetupPackageBase import *

class Package(SetupPackageBase):
    def __init__( self):
        SetupPackageBase.__init__(self)
            
if __name__ == '__main__':
    Package().execute()
