import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/extragear/network/ktorrent'
        for version in ['3.2beta1', '3.2rc1', '3.2', '3.2.2', '3.2.3', '3.3beta1']:
            self.targets[version] = 'http://ktorrent.org/downloads/' + version + '/ktorrent-' + version + '.tar.bz2'
            self.targetInstSrc[version] = 'ktorrent-' + version
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kde/kdepimlibs'] = 'default'
        self.hardDependencies['kdesupport/qca'] = 'default'
        self.hardDependencies['win32libs-bin/libgmp'] = 'default'
        self.hardDependencies['dev-util/gettext-tools'] = 'default'
    
class Package(CMakePackageBase):
    def __init__( self):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
