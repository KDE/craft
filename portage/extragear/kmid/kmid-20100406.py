import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/multimedia/kmid'
        for ver in ['2.3.0', '2.3.1']:
          self.targets[ver] = 'http://downloads.sourceforge.net/kmid2/kmid-' + ver + '.tar.bz2'
          self.targetInstSrc[ver] = 'kmid-' + ver
        self.defaultTarget = '2.3.1'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
    
class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
