import info
import compiler
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kde-runtime|KDE/4.7|'
        for ver in ['0', '1', '2', '3', '4']:
            self.targets['4.7.' + ver] = "ftp://ftp.kde.org/pub/kde/stable/4.7." + ver + "/src/kde-runtime-4.7." + ver + ".tar.bz2"
            self.targetInstSrc['4.7.' + ver] = 'kde-runtime-4.7.' + ver
        self.defaultTarget = 'gitHEAD'

    def setDependencies( self ):
        self.dependencies['kde/kdelibs'] = 'default'
        self.dependencies['kdesupport/oxygen-icons'] = 'default'
        self.dependencies['win32libs-bin/libssh'] = 'default'
        if compiler.isMinGW_WXX():
#            self.dependencies['win32libs-bin/libbfd'] = 'default'
            self.dependencies['win32libs-sources/libbfd-src'] = 'default'
        self.shortDescription = "Plugins and applications necessary for the running of KDE applications."

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
