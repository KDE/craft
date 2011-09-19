import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdepim-runtime'
        for version in ['4.4', '4.5', '4.6', '4.7', '4.8', '4.9']:
            self.svnTargets[version] = '[git]kde:kdepim-runtime|KDE/%s' % version
        self.defaultTarget = '4.7'
        self.patchToApply['4.7'] = ('Disable-ServerSide-subscriptions-by-default.patch', 1)

    def setDependencies( self ):
        self.dependencies['enterprise5/kderuntime-e5'] = 'default'
        self.dependencies['kdesupport/oxygen-icons'] = 'default'
        self.dependencies['enterprise5/kdepimlibs-e5'] = 'default'
        self.dependencies['enterprise5/grantlee-e5'] = 'default'
        self.dependencies['win32libs-bin/sqlite'] = 'default'

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DKLEO_SYNCHRONOUS_API_HOTFIX=ON "

        self.subinfo.options.configure.defines += " -DKDE4_BUILD_TESTS=OFF "
        self.subinfo.options.configure.defines += " -DKDEPIM_ENTERPRISE_BUILD=ON "
        self.subinfo.options.configure.defines += " -DKDEPIM_BUILD_MOBILE=FALSE "
        self.subinfo.options.configure.defines += " -DACCOUNTWIZARD_NO_GHNS=TRUE "

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
