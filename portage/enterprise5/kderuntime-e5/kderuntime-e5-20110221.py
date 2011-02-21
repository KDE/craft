import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = '[git]kde:kde-runtime|KDE/4.6|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.6.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.6.' + ver + '/src/kdebase-runtime-4.6.' + ver + '.tar.bz2'
            self.targetInstSrc['4.6.' + ver] = 'kdebase-runtime-4.6.' + ver
        self.defaultTarget = '4.6.0'
    
    def setDependencies( self ):
        self.dependencies['enterprise5/kdelibs-e5'] = 'default'
        self.dependencies['kdesupport/oxygen-icons'] = 'default'
        self.dependencies['enterprise5/phonon-vlc-e5'] = 'default'
        self.dependencies['win32libs-sources/libssh-src'] = 'default'
        self.dependencies['win32libs-sources/libbfd-src'] = 'default'
        self.shortDescription = "KDE runtime libraries"

from Package.CMakePackageBase import *
        
class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = (
                " -DBUILD_doc=OFF " )

if __name__ == '__main__':
    Package().execute()
