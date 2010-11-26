import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/multimedia/k3b'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['virtual/kdebase-runtime'] = 'default'
        self.dependencies['virtual/kdemultimedia'] = 'default'
        self.dependencies['testing/libsamplerate'] = 'default'
        self.dependencies['testing/libdvdcss'] = 'default'
        #        self.dependencies['testing/libcdio'] = 'default'
        
class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
