import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdepimlibs|4.7|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.7.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.7.' + ver + '/src/kdepimlibs-4.7.' + ver + '.tar.bz2'
            self.targetInstSrc['4.7.' + ver] = 'kdepimlibs-4.7.' + ver
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kdesupport/akonadi'] = 'default'
        self.dependencies['win32libs-bin/cyrus-sasl'] = 'default'
        self.dependencies['win32libs-bin/libical'] = 'default'
        self.dependencies['win32libs-bin/boost'] = 'default'
        self.dependencies['win32libs-bin/gpgme'] = 'default'
        self.shortDescription = "the base libraries for PIM related services"


    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.boost = portage.getPackageInstance('win32libs-bin','boost')
        path = self.boost.installDir()
        os.putenv( "BOOST_ROOT", path )

        self.subinfo.options.configure.defines += "-DBUILD_doc=OFF "

if __name__ == '__main__':
    Package().execute()
