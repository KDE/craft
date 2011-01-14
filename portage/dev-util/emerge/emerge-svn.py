import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/emerge'
        self.svnTargets['refactoring-2010'] = 'branches/work/emerge/refactoring-2010'
        self.svnTargets['1.0'] = 'tags/emerge/1.0'
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'

from Package.PackageBase import *
from Source.SvnSource import *
from BuildSystem.BuildSystemBase import *
from datetime import date

class Package(PackageBase,SvnSource,BuildSystemBase):
    def __init__( self):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        SvnSource.__init__(self)
        BuildSystemBase.__init__(self,"")

    def checkoutDir(self, index=0 ):
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
