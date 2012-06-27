import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdepimlibs|KDE/4.8|'
        
        self.targets['4.8.0'] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.0/src/kdepimlibs-4.8.0.tar.bz2'
        self.targetInstSrc['4.8.0'] = 'kdepimlibs-4.8.0'
        self.patchToApply['4.8.0'] = [("kdepimlibs-4.8.0-20120206.diff", 1)]
        
        for ver in ['1', '2', '3', '4']:
            self.targets['4.8.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.8.' + ver + '/src/kdepimlibs-4.8.' + ver + '.tar.xz'
            self.targetInstSrc['4.8.' + ver] = 'kdepimlibs-4.8.' + ver
        
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        #self.dependencies['kdesupport/akonadi'] = 'default'
        self.dependencies['win32libs-bin/cyrus-sasl'] = 'default'
        self.dependencies['win32libs-bin/libical'] = 'default'
        self.dependencies['win32libs-bin/gpgme'] = 'default'
        self.dependencies['win32libs-bin/openldap'] = 'default'
        self.shortDescription = "the base libraries for PIM related services"

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
