import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.5/kdepimlibs'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.5.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.5.' + ver + '/src/kdepimlibs-4.5.' + ver + '.tar.bz2'
            self.targetInstSrc['4.5.' + ver] = 'kdepimlibs-4.5.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['kde-4.5/kdelibs'] = 'default'
        self.dependencies['kdesupport/akonadi'] = 'default'
        self.dependencies['win32libs-bin/cyrus-sasl'] = 'default'
        self.dependencies['win32libs-bin/libical'] = 'default'
        self.dependencies['win32libs-bin/boost'] = 'default'
        self.dependencies['win32libs-bin/gpgme'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.boost = portage.getPackageInstance('win32libs-bin','boost')
        path = self.boost.installDir()
        os.putenv( "BOOST_ROOT", path )

if __name__ == '__main__':
    Package().execute()
