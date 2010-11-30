import info
from Package.CMakePackageBase import *

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = 'git://gitorious.org/kmess/kmess.git'
        self.defaultTarget = 'gitHEAD'
    
    def setDependencies( self ):
        self.dependencies['virtual/kdebase-runtime'] = 'default'
        self.dependencies['testing/libgcrypt-src'] = 'default'
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        
if __name__ == '__main__':
    Package().execute()