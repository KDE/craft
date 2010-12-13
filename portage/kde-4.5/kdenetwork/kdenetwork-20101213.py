import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.5/kdenetwork'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.5.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.5.' + ver + '/src/kdenetwork-4.5.' + ver + '.tar.bz2'
            self.targetInstSrc['4.5.' + ver] = 'kdenetwork-4.5.' + ver
        self.defaultTarget = 'svnHEAD'
        self.patchToApply['4.5.4'] = ( 'kdenetwork-4.5.4-20101213.diff', 1 )
    
    def setDependencies( self ):
        self.dependencies['kde-4.5/kdebase-runtime'] = 'default'
        self.dependencies['kde-4.5/kdepimlibs'] = 'default'
        self.dependencies['kdesupport/qca'] = 'default'
        self.dependencies['win32libs-bin/libidn'] = 'default'
        self.dependencies['win32libs-bin/libmsn'] = 'default'
#        self.dependencies['win32libs-bin/libgmp'] = 'default'
        
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
