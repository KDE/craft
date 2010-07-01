import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.5'] = 'branches/KDE/4.5/kdenetwork'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdenetwork'
        self.defaultTarget = '4.5'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.5/kdebase-runtime'] = 'default'
        self.hardDependencies['kde-4.5/kdepimlibs'] = 'default'
        self.hardDependencies['kdesupport/qca'] = 'default'
        self.hardDependencies['win32libs-bin/libidn'] = 'default'
        self.hardDependencies['win32libs-bin/libmsn'] = 'default'
        self.hardDependencies['win32libs-bin/libgmp'] = 'default'
        
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
