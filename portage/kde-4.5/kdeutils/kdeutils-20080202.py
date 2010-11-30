import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.5/kdeutils'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.5.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.5.' + ver + '/src/kdeutils-4.5.' + ver + '.tar.bz2'
            self.targetInstSrc['4.5.' + ver] = 'kdeutils-4.5.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['kde-4.5/kdebase-runtime'] = 'default'
        self.dependencies['kde-4.5/kdepimlibs'] = 'default'
#        self.dependencies['win32libs-bin/libgmp'] = 'default'
        self.dependencies['win32libs-bin/libzip'] = 'default'
        self.dependencies['win32libs-bin/libarchive'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        #        self.subinfo.options.configure.defines += "-DBUILD_kwallet=OFF "
        #        self.subinfo.options.configure.defines += "-DBUILD_doc=OFF"

if __name__ == '__main__':
    Package().execute()

