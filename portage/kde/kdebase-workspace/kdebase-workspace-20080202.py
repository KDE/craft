import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdebase/workspace'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdebase/workspace'
        self.svnTargets['komobranch'] = 'branches/work/komo/kdebase/workspace'
        for ver in ['80', '83', '85']:
            self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdebase-workspace-4.0.' + ver + '.tar.bz2'
            self.targetInstSrc['4.0.' + ver] = 'kdebase-workspace-4.0.' + ver
        if platform.isCrossCompilingEnabled():
            self.defaultTarget = 'komobranch'
        else:
            self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kde/kdelibs'] = 'default'
        if not platform.isCrossCompilingEnabled():
            self.hardDependencies['win32libs-bin/fontconfig'] = 'default'
        self.hardDependencies['win32libs-bin/freetype'] = 'default'
        self.hardDependencies['win32libs-bin/boost'] = 'default'
        self.hardDependencies['kdesupport/akonadi'] = 'default'
    
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

