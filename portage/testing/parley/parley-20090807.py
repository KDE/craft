import info
       
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = "trunk/KDE/kdeedu#norecursive;trunk/KDE/kdeedu/parley;trunk/KDE/kdeedu/cmake"
        self.svnTargets['branches-4.3'] = "branches/KDE/4.3/kdeedu#norecursive;branches/KDE/4.3/kdeedu/parley;branches/KDE/4.3/kdeedu/cmake"        
        
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.3.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.3.' + ver + '/src/kdeedu-4.3.' + ver + '.tar.bz2'
            self.targetInstSrc['4.3.' + ver] = 'kdeedu-4.3.' + ver
        self.defaultTarget = 'svnHEAD'

        
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kdesupport/kdewin'] = 'default'
        self.hardDependencies['kdesupport/oxygen-icons'] = 'default'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.onlyBuildTargets = 'parley' 
        self.subinfo.options.make.slnBaseName = 'kdeedu' 
            
if __name__ == '__main__':
    Package().execute()

    
