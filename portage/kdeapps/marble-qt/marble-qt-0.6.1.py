import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdeedu/marble'
        self.svnTargets['0.5.1'] = 'branches/KDE/4.0/kdeedu/marble'
        self.svnTargets['0.6.1'] = 'branches/KDE/4.1/kdeedu/marble'
        self.svnTargets['0.7.1'] = 'branches/KDE/4.2/kdeedu/marble'
        self.svnTargets['0.8.0'] = 'tags/marble/0.8.0'
        self.svnTargets['0.9.2'] = 'branches/KDE/4.4/kdeedu/marble'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['libs/qt'] = 'default'
        
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        self.subinfo.options.configure.defines = "-DQTONLY=ON -DBUILD_MARBLE_TESTS=OFF"
        CMakePackageBase.__init__(self)

if __name__ == '__main__':
    Package().execute()
