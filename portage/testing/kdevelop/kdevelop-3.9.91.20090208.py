import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/sdk/kdevelop'
        self.svnTargets['3.9.94'] = 'tags/kdevelop/3.9.94'
        self.svnTargets['3.9.96'] = 'tags/kdevelop/3.9.96'
        self.defaultTarget = 'svnHEAD'
    
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
