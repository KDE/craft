import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.3/kdewebdev'
        for ver in ['91', '95', '98']:
          self.targets['4.2.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.2.' + ver + '/src/kdewebdev-4.2.' + ver + '.tar.bz2'
          self.targetInstSrc['4.2.' + ver] = 'kdewebdev-4.2.' + ver
        for ver in ['0', '1', '2', '3', '4']:
          self.targets['4.3.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.3.' + ver + '/src/kdewebdev-4.3.' + ver + '.tar.bz2'
          self.targetInstSrc['4.3.' + ver] = 'kdewebdev-4.3.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.3/kdebase-runtime'] = 'default'
        self.softDependencies['kde-4.3/kdevplatform'] = 'default'
        
from Package.CmakePackageBase import *        
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        # if you want to build quanta, you need to build kdevplatform as well - this is not build by default!!!
        self.subinfo.options.configure.defines += "-DBUILD_quanta=OFF "
        self.subinfo.options.configure.defines += "-DBUILD_kfilereplace=OFF "
        self.subinfo.options.configure.defines += "-DBUILD_kxsldbg=OFF "
        self.subinfo.options.configure.defines += "-DBUILD_kommander=OFF "

if __name__ == '__main__':
    Package().execute()
