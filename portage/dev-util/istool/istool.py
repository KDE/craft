import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['5.3.0.1'] = ' http://netcologne.dl.sourceforge.net/project/istool/istool-5.3.0.1.exe'
        self.defaultTarget = '5.3.0.1'

from Package.SetupPackageBase import *

class Package(SetupPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        SetupPackageBase.__init__(self)
            
if __name__ == '__main__':
    Package().execute()
