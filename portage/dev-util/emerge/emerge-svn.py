import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/emerge'
        self.defaultTarget = 'svnHEAD'

from Package.PackageBase import *
from Source.SvnSource import *
from BuildSystem.BuildSystemBase import *

class Package(PackageBase,SvnSource,BuildSystemBase):
    def __init__( self):
        self.subinfo = subinfo()
        self.subinfo.options.merge.destinationPath = "."
        PackageBase.__init__(self)
        SvnSource.__init__(self)
        BuildSystemBase.__init__(self,"")

    def sourceDir(self, index=0 ): 
        return os.path.join(ROOTDIR,"emerge")

    def configure(self):
        return True

    def make(self):
        return True
        
    def install(self): 
        return True

    def qmerge(self):
        return True

    def createPackage(self):
        return True

if __name__ == '__main__':
    Package().execute()
