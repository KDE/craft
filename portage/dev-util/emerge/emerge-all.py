import info

class subinfo(info.infoclass):
    def setTargets( self ):
        for ver in ['4.6', '4.7', '4.8', '4.9', '4.10']:
            self.svnTargets[ver] = '[git]kde:emerge|kde-' + ver + '|'
        self.svnTargets['gitHEAD'] = '[git]kde:emerge'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['virtual/base'] = 'default'

from Package.CMakePackageBase import *
from BuildSystem.BuildSystemBase import *


class Package(PackageBase,GitSource,BuildSystemBase):
    def __init__( self):
        self.subinfo = subinfo()
        PackageBase.__init__(self)
        GitSource.__init__(self)
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
