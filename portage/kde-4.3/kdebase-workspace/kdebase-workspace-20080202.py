# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *        


class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'branches/KDE/4.3/kdebase/workspace'
        for ver in ['91', '95', '98']:
          self.targets['4.2.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.2.' + ver + '/src/kdebase-workspace-4.2.' + ver + '.tar.bz2'
          self.targetInstSrc['4.2.' + ver] = 'kdebase-workspace-4.2.' + ver
        for ver in ['0', '1', '2', '3', '4']:
          self.targets['4.3.' + ver] = 'ftp://ftp.kde.org/pub/kde/stable/4.3.' + ver + '/src/kdebase-workspace-4.3.' + ver + '.tar.bz2'
          self.targetInstSrc['4.3.' + ver] = 'kdebase-workspace-4.3.' + ver
        self.patchToApply['4.2.95'] = ( 'kdebase-kworkspace.diff', 0 )
        self.patchToApply['4.3.0'] = ( 'kdebase-workspace-tasks.diff', 0 )
        self.patchToApply['4.3.1'] = ( 'kdebase-workspace-tasks.diff', 0 )
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kde-4.3/kdelibs'] = 'default'
        self.hardDependencies['kde-4.3/kdepimlibs'] = 'default'
        self.hardDependencies['kde-4.3/kdebase-runtime'] = 'default'
        self.hardDependencies['win32libs-bin/fontconfig'] = 'default'
        self.hardDependencies['win32libs-bin/freetype'] = 'default'

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.configure.onlyBuildTargets = "systemsettings krunner khotkeys kcontrol plasma doc wallpapers"

if __name__ == '__main__':
    Package().execute()
