import info

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdepim-runtime|4.7|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.7.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.7." + ver + "/src/kdepim-runtime-4.7." + ver + ".tar.bz2"
            self.targetInstSrc['4.7.' + ver] = 'kdepim-runtime-4.7.' + ver
        self.patchToApply['4.7.0'] = ("kdepim-runtime-4.7.0-20110823.diff", 1)
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['kde/kdepimlibs'] = 'default'
        self.dependencies['kdesupport/grantlee'] = 'default'
        self.dependencies['win32libs-bin/sqlite'] = 'default'
        self.shortDescription = "Extends the functionality of kdepim"

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = True

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DKLEO_SYNCHRONOUS_API_HOTFIX=ON "
        self.subinfo.options.configure.defines += " -DKDEPIM_BUILD_MOBILE=FALSE "
        self.subinfo.options.configure.defines += "-DBUILD_doc=OFF "

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
