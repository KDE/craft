# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdelibs'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdelibs'
        self.defaultTarget = '20091123'
    
    def setDependencies( self ):
        self.hardDependencies['enterprise5/kdewin-e5'] = 'default'
        self.hardDependencies['enterprise5/qimageblitz-e5'] = 'default'
        self.hardDependencies['enterprise5/soprano-e5'] = 'default'
        self.hardDependencies['enterprise5/strigi-e5'] = 'default'
        self.hardDependencies['enterprise5/phonon-e5'] = 'default'
        self.hardDependencies['enterprise5/automoc-e5'] = 'default'
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
        elif self.compiler() == "mingw4":
          self.subinfo.options.configure.defines = " -DKDE_DISTRIBUTION_TEXT=\"MinGW 4.4.0\" "
        elif self.compiler() == "msvc2005":
          self.subinfo.options.configure.defines = " -DKDE_DISTRIBUTION_TEXT=\"MS Visual Studio 2005 SP1\" "
        elif self.compiler() == "msvc2008":
          self.subinfo.options.configure.defines = " -DKDE_DISTRIBUTION_TEXT=\"MS Visual Studio 2008 SP1\" "

if __name__ == '__main__':
    Package().execute()
