# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdepim'
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdepim'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdepim-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdepim-4.0.' + ver
        self.defaultTarget = 'svnHEAD'

    def setDependencies( self ):
        self.hardDependencies['kde/kdebase-runtime'] = 'default'
        self.hardDependencies['kde/kdepimlibs'] = 'default'
        self.hardDependencies['kdesupport/grantlee'] = 'default'
        self.hardDependencies['win32libs-bin/sqlite'] = 'default'
        
    def setBuildOptions( self ):
        self.disableHostBuild = True
        self.disableTargetBuild = False

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = "-DKLEO_SYNCHRONOUS_API_HOTFIX=ON "
        if self.isTargetBuild():
            self.subinfo.options.configure.defines += " -DBUILD_kleopatra=OFF "
            self.subinfo.options.configure.defines += " -DBUILD_blogilo=OFF "
            self.subinfo.options.configure.defines += " -DBUILD_kjots=OFF "
            self.subinfo.options.configure.defines += " -DBUILD_knotes=OFF "
            self.subinfo.options.configure.defines += " -DBUILD_kaddressbook=OFF "
            self.subinfo.options.configure.defines += " -DKDEPIM_MOBILE_UI=TRUE "

        if platform.isCrossCompilingEnabled():
            self.subinfo.options.configure.defines += " -DBUILD_doc=OFF "
            
        
        self.subinfo.options.configure.defines += "-DHOST_BINDIR=%s " \
            % os.path.join(ROOTDIR, "bin")

if __name__ == '__main__':
    Package().execute()
