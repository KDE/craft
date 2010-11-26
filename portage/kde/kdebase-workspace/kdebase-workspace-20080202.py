import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdebase/workspace'
        self.svnTargets['komobranch'] = 'branches/work/komo/kdebase/workspace'
        if emergePlatform.isCrossCompilingEnabled():
            self.defaultTarget = 'komobranch'
        else:
            self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.dependencies['kde/kdebase-runtime'] = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs-bin/fontconfig'] = 'default'
        self.dependencies['win32libs-bin/freetype'] = 'default'
        self.dependencies['win32libs-bin/boost'] = 'default'
        self.dependencies['kdesupport/akonadi'] = 'default'
    
    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
        self.subinfo.options.configure.defines += "-DHOST_BINDIR=%s " \
            % os.path.join(ROOTDIR, "bin")
        if self.isTargetBuild():
            self.subinfo.options.configure.defines += "-DDISABLE_ALL_OPTIONAL_SUBDIRECTORIES=TRUE "

if __name__ == '__main__':
    Package().execute()

