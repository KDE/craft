import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdepimlibs'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdepimlibs'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdepimlibs'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdepimlibs'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdepimlibs'
        self.defaultTarget = '20100115'
    
    def setDependencies( self ):
        self.hardDependencies['enterprise5/kdelibs-e5'] = 'default'
        self.hardDependencies['enterprise5/akonadi-e5'] = 'default'
        self.hardDependencies['win32libs-sources/cyrus-sasl-src'] = 'default'
        self.hardDependencies['win32libs-sources/boost-src'] = 'default'
        self.hardDependencies['win32libs-sources/libical-src'] = 'default'
        self.hardDependencies['win32libs-bin/gpgme'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
