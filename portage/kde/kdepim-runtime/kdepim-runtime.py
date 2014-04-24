import info
import kdedefaults as kd
from emerge_config import *

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:%s|%s|' % (self.package, kd.kdebranch)
        for ver in ['0', '1', '2', '3', '4', '5']:
            self.targets[kd.kdeversion + ver] = "http://download.kde.org/stable/" + kd.kdeversion + ver + "/src/" + self.package + "-" + kd.kdeversion + ver + ".tar.xz"
            self.targetInstSrc[kd.kdeversion + ver] = self.package + '-' + kd.kdeversion + ver
            self.targetDigestUrls[ kd.kdeversion + ver  ] = 'http://download.kde.org/stable/' + kd.kdeversion + ver + '/src/' + self.package + '-' + kd.kdeversion + ver + '.tar.xz.sha1'
            self.patchToApply[kd.kdeversion + ver] = [("kdepim-runtime-4.10.2-20130531.diff", 1), # not to be upstreamed, this fix is only a hack
                                                      ("0001-fixed-windows-build.patch", 1), # reverted upstream (test on Linux first / too near to release tag to test)
                                                      ("0002-fix-akonadi_serializer_kcalcore-build-on-msvc.patch", 1)] # TODO: test and commit upstream

        
        self.patchToApply['gitHEAD'] = [("kdepim-runtime-4.10.2-20130531.diff", 1), # not to be upstreamed, this fix is only a hack
                                        ("0001-fixed-windows-build.patch", 1), # reverted upstream (test on Linux first / too near to release tag to test)
                                        ("0002-fix-akonadi_serializer_kcalcore-build-on-msvc.patch", 1)] # TODO: test and commit upstream

        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['kdesupport/grantlee'] = 'default'
        self.dependencies['win32libs/sqlite'] = 'default'
        self.dependencies['extragear/libkolab'] = 'default'
        self.dependencies['extragear/libkgapi'] = 'default'
        self.dependencies['extragear/libkfbapi'] = 'default'
        self.shortDescription = "Extends the functionality of kdepim"

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

    def install( self ):
        if not CMakePackageBase.install( self ):
            return False
        if compiler.isMinGW():
            manifest = os.path.join( self.packageDir(), "akonadi_maildispatcher_agent.exe.manifest" )
            executable = os.path.join( self.installDir(), "bin", "akonadi_maildispatcher_agent.exe" )
            utils.embedManifest( executable, manifest )
        return True

if __name__ == '__main__':
    Package().execute()
