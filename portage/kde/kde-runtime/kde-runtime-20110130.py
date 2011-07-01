import info
import compiler
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kde-runtime|KDE/4.7|'
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
