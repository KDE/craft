import info
import kdedefaults as kd

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:%s|%s|' % (self.package, kd.kdebranch)
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets[kd.kdeversion + ver] = "http://download.kde.org/stable/" + kd.kdeversion + ver + "/src/" + self.package + "-" + kd.kdeversion + ver + ".tar.xz"
            self.targetInstSrc[kd.kdeversion + ver] = self.package + '-' + kd.kdeversion + ver
        self.patchToApply['4.10.0'] = [('kdepimlibs-4.10.0.diff', 1)]
        self.patchToApply['4.10.1'] = [('kdepimlibs-4.10.0.diff', 1)]
        self.patchToApply['4.10.2'] = [('kdepimlibs-4.10.0.diff', 1)]
        self.patchToApply['4.10.4'] = [('kdepimlibs-4.10.0.diff', 1)]

        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kde/nepomuk-core'] = 'default'
        self.dependencies['kdesupport/akonadi'] = 'default'
        self.dependencies['win32libs/cyrus-sasl'] = 'default'
        self.dependencies['win32libs/libical'] = 'default'
        self.dependencies['win32libs/gpgme'] = 'default'
        self.dependencies['win32libs/openldap'] = 'default'
        self.dependencies['win32libs/boost-graph'] = 'default'
        
        self.shortDescription = "the base libraries for PIM related services"

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.boost = portage.getPackageInstance('win32libs','boost')
        path = self.boost.installDir()
        os.putenv( "BOOST_ROOT", path )

if __name__ == '__main__':
    Package().execute()
