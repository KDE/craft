import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/kdevelop/kdevelop.git'
        self.defaultTarget = 'gitHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['testing/kdevplatform'] = 'default'
        self.hardDependencies['dev-util/zip'] = 'default'
    
from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
