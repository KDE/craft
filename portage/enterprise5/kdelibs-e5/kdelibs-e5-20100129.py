# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdelibs'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdelibs'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdelibs'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdelibs'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdelibs'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdelibs'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdelibs'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdelibs'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdelibs'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdelibs'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdelibs'
        self.defaultTarget = '20100129'
    
    def setDependencies( self ):
        self.hardDependencies['enterprise5/kdewin-e5'] = 'default'
        self.hardDependencies['enterprise5/qimageblitz-e5'] = 'default'
        self.hardDependencies['enterprise5/soprano-e5'] = 'default'
        self.hardDependencies['enterprise5/strigi-e5'] = 'default'
        self.hardDependencies['enterprise5/phonon-e5'] = 'default'
        self.hardDependencies['enterprise5/automoc-e5'] = 'default'

        self.hardDependencies['win32libs-sources/bzip2-src']  = 'default'
        self.hardDependencies['win32libs-sources/libpng-src']  = 'default'
        self.hardDependencies['win32libs-sources/openssl-src']  = 'default'
        self.hardDependencies['win32libs-sources/pcre-src']  = 'default'
        self.hardDependencies['win32libs-sources/shared-desktop-ontologies-src'] = 'default'
# binary packages only
        self.hardDependencies['win32libs-bin/giflib']  = 'default'
        self.hardDependencies['win32libs-bin/jpeg']  = 'default'
        self.hardDependencies['win32libs-bin/libxml2']  = 'default'
        self.hardDependencies['win32libs-bin/libxslt']  = 'default'
        self.hardDependencies['win32libs-bin/zlib']  = 'default'
# check if the MSYS dependency for building aspell-src can be removed
        self.hardDependencies['win32libs-bin/aspell']  = 'default'
# gettext-src uses a weird shell script for building
        self.hardDependencies['win32libs-bin/gettext']  = 'default'
        
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['dev-util/perl'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['win32libs-bin/shared-mime-info']  = 'default'
        self.hardDependencies['data/aspell-data'] = 'default'

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
