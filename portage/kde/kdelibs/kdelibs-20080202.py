# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/KDE/kdelibs'
        self.svnTargets['4.0.0'] = 'tags/KDE/4.0.0/kdelibs'
        for ver in ['80', '83', '85']:
          self.targets['4.0.' + ver] = 'ftp://ftp.kde.org/pub/kde/unstable/4.0.' + ver + '/src/kdelibs-4.0.' + ver + '.tar.bz2'
          self.targetInstSrc['4.0.' + ver] = 'kdelibs-4.0.' + ver
        self.defaultTarget = 'svnHEAD'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/kdewin'] = 'default'
        self.hardDependencies['kdesupport/qimageblitz'] = 'default'
        self.hardDependencies['kdesupport/soprano'] = 'default'
        self.hardDependencies['kdesupport/strigi'] = 'default'
        self.hardDependencies['kdesupport/phonon'] = 'default'
        self.hardDependencies['kdesupport/automoc'] = 'default'
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/perl'] = 'default'
        self.hardDependencies['virtual/kdelibs-base'] = 'default'

from Package.CMakePackageBase import *
        
class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        if self.compiler() == "mingw":
          self.subinfo.options.configure.defines = " -DKDE_DISTRIBUTION_TEXT=\"MinGW 3.4.5\" "
        elif self.compiler() == "msvc2005":
          self.subinfo.options.configure.defines = " -DKDE_DISTRIBUTION_TEXT=\"MS Visual Studio 2005 SP1\" "
        elif self.compiler() == "msvc2008":
          self.subinfo.options.configure.defines = " -DKDE_DISTRIBUTION_TEXT=\"MS Visual Studio 2008 SP1\" "

if __name__ == '__main__':
    Package().execute()
