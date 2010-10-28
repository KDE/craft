import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.targets['2.26.3'] = 'http://www.graphviz.org/pub/graphviz/stable/windows/graphviz-2.26.3.msi'
        self.targetDigests['2.26.3'] = '0ce70fcd7ce880ee19ecce6ef8e943d48a1a5374'
        self.defaultTarget = '2.26.3'
        # the zip file does not have a bin dir, so we have to create it  
        # This attribute is in prelimary state
        #self.targetInstallPath['1.5.9'] = "bin"
        
from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.ignoreBuildType = True
        self.subinfo.options.merge.destinationPath = "dev-utils"
        BinaryPackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
