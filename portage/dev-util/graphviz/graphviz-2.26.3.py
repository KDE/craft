import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['2.26.3'] = 'http://www.graphviz.org/pub/graphviz/stable/windows/graphviz-2.26.3.msi'
        self.defaultTarget = '2.26.3'
        
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
