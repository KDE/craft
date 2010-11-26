import compiler
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdenetwork'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['kde/kdebase-runtime'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['win32libs-bin/libidn'] = 'default'
        self.dependencies['win32libs-bin/libmsn'] = 'default'
        #mingw already contains libgmp
        if not compiler.isMinGW():
            self.dependencies['win32libs-bin/libgmp'] = 'default'
        
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
