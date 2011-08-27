import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kde-workspace|KDE/4.7|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.7.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.7." + ver + "/src/kde-workspace-4.7." + ver + ".tar.bz2"
            self.targetInstSrc['4.7.' + ver] = 'kde-workspace-4.7.' + ver
        self.patchToApply['4.7.0'] = ("kde-workspace-4.7.0-20110822.diff", 1)
        self.shortDescription = 'the KDE workspace including the oxygen style'
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kde-runtime'] = 'default'
        self.dependencies['win32libs-bin/freetype'] = 'default'
        self.dependencies['kdesupport/akonadi'] = 'default'#boost is a implicit dependency by akonadi

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        self.subinfo.options.configure.defines += "-DBUILD_doc=OFF "

if __name__ == '__main__':
    Package().execute()

