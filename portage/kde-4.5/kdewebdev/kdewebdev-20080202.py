import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdewebdev'
        self.svnTargets['4.5'] = 'tags/KDE/4.0.0/kdewebdev'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdewebdev'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdewebdev-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdewebdev-4.0.' + ver
        self.defaultTarget = '4.5'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.5/kdelibs'] = 'default'
        self.hardDependencies['kde-4.5/kdepimlibs'] = 'default'
        self.hardDependencies['kde-4.5/kdebase-runtime'] = 'default'
        #self.softDependencies['kde/kdevplatform'] = 'default'
        
from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        # if you want to build quanta, you need to build kdevplatform as well - this is not build by default!!!
        self.subinfo.options.configure.defines = ""
        self.subinfo.options.configure.defines += "-DBUILD_kfilereplace=OFF "
        self.subinfo.options.configure.defines += "-DBUILD_kxsldbg=OFF "
        self.subinfo.options.configure.defines += "-DBUILD_kommander=OFF "

if __name__ == '__main__':
    Package().execute()
