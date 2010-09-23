import info
import compiler
class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdebase/runtime'
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdelibs'] = 'default'
        self.hardDependencies['kdesupport/oxygen-icons'] = 'default'
        if not platform.isCrossCompilingEnabled():
            self.hardDependencies['win32libs-sources/libssh-src'] = 'default'
        if compiler.isMinGW_WXX():
            self.hardDependencies['win32libs-sources/binutils-src'] = 'default'

    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        if platform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines += "-DDISABLE_ALL_OPTIONAL_SUBDIRECTORIES=TRUE "
        
        self.subinfo.options.configure.defines += "-DHOST_BINDIR=%s " \
            % os.path.join(ROOTDIR, "bin")
            
        if self.isTargetBuild():
            self.subinfo.options.configure.defines += "-DKDEBASE_DISABLE_MULTIMEDIA=ON "

if __name__ == '__main__':
    Package().execute()
