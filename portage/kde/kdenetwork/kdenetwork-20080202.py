import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdenetwork'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kde/kdepimlibs'] = 'default'
        self.hardDependencies['kdesupport/qca'] = 'default'
        self.hardDependencies['win32libs-sources/libidn-src'] = 'default'
        self.hardDependencies['win32libs-bin/libmsn'] = 'default'
        self.hardDependencies['win32libs-bin/libgmp'] = 'default'
        
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
