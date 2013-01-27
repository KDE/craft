import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdepimlibs|KDE/4.9|'
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets['4.9.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.9.' + ver + '/src/kdepimlibs-4.9.' + ver + '.tar.xz'
            self.targetInstSrc['4.9.' + ver] = 'kdepimlibs-4.9.' + ver
        self.shortDescription = "the base libraries for PIM related services"
        self.patchToApply['gitHEAD'] = [("kdepimlibs-4.9.diff", 1)]
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kdesupport/akonadi'] = 'default'
        self.dependencies['win32libs-bin/cyrus-sasl'] = 'default'
        self.dependencies['win32libs-bin/libical'] = 'default'
        self.dependencies['win32libs-bin/gpgme'] = 'default'
        self.dependencies['win32libs-bin/openldap'] = 'default'

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
