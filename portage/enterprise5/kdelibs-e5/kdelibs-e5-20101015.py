# -*- coding: utf-8 -*-
import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdelibs'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdelibs'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdelibs'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdelibs'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdelibs'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdelibs'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdelibs'
        self.svnTargets['20100205'] = 'tags/kdepim/enterprise5.0.20100205.1085631/kdelibs'
        self.svnTargets['20100212'] = 'tags/kdepim/enterprise5.0.20100212.1089060/kdelibs'
        self.svnTargets['20100219'] = 'tags/kdepim/enterprise5.0.20100219.1092868/kdelibs'
        self.svnTargets['20100226'] = 'tags/kdepim/enterprise5.0.20100226.1096279/kdelibs'
        self.svnTargets['20100305'] = 'tags/kdepim/enterprise5.0.20100305.1099232/kdelibs'
        self.svnTargets['20100312'] = 'tags/kdepim/enterprise5.0.20100312.1102371/kdelibs'
        self.svnTargets['20100319'] = 'tags/kdepim/enterprise5.0.20100319.1105074/kdelibs'
        self.svnTargets['20100326'] = 'tags/kdepim/enterprise5.0.20100326.1107645/kdelibs'
        self.svnTargets['20100401'] = 'tags/kdepim/enterprise5.0.20100401.1110042/kdelibs'
        self.svnTargets['20100409'] = 'tags/kdepim/enterprise5.0.20100409.1112952/kdelibs'
        self.svnTargets['20100507'] = 'tags/kdepim/enterprise5.0.20100507.1123982/kdelibs'
        self.svnTargets['20100528'] = 'tags/kdepim/enterprise5.0.20100528.1131643/kdelibs'
        self.svnTargets['20100604'] = 'tags/kdepim/enterprise5.0.20100604.1134428/kdelibs'
        self.svnTargets['20100611'] = 'tags/kdepim/enterprise5.0.20100611.1136974/kdelibs'
        self.svnTargets['20100618'] = 'tags/kdepim/enterprise5.0.20100618.1139547/kdelibs'
        self.svnTargets['20100625'] = 'tags/kdepim/enterprise5.0.20100625.1142603/kdelibs'
        self.svnTargets['20100701'] = 'tags/kdepim/enterprise5.0.20100701.1144979/kdelibs'
        self.svnTargets['20100709'] = 'tags/kdepim/enterprise5.0.20100709.1148001/kdelibs'
        self.svnTargets['20100716'] = 'tags/kdepim/enterprise5.0.20100716.1150616/kdelibs'
        self.svnTargets['20100723'] = 'tags/kdepim/enterprise5.0.20100723.1153624/kdelibs'
        self.svnTargets['20100730'] = 'tags/kdepim/enterprise5.0.20100730.1157241/kdelibs'
        self.svnTargets['20100805'] = 'tags/kdepim/enterprise5.0.20100805.1159431/kdelibs'
        self.svnTargets['20100813'] = 'tags/kdepim/enterprise5.0.20100813.1163234/kdelibs'
        self.svnTargets['20100820'] = 'tags/kdepim/enterprise5.0.20100820.1165957/kdelibs'
        self.svnTargets['20100827'] = 'tags/kdepim/enterprise5.0.20100827.1168749/kdelibs'
        self.svnTargets['20100903'] = 'tags/kdepim/enterprise5.0.20100903.1171282/kdelibs'
        self.svnTargets['20100910'] = 'tags/kdepim/enterprise5.0.20100910.1173808/kdelibs'
        self.svnTargets['20100917'] = 'tags/kdepim/enterprise5.0.20100917.1176291/kdelibs'
        self.svnTargets['20100927'] = 'tags/kdepim/enterprise5.0.20100927.1180225/kdelibs'
        self.svnTargets['20101001'] = 'tags/kdepim/enterprise5.0.20101001.1181557/kdelibs'
        self.svnTargets['20101008'] = 'tags/kdepim/enterprise5.0.20101008.1183806/kdelibs'
        self.svnTargets['20101015'] = 'tags/kdepim/enterprise5.0.20101015.1186246/kdelibs'
        self.defaultTarget = '20101015'
    
    def setDependencies( self ):
        self.hardDependencies['enterprise5/kdewin-e5'] = 'default'
        self.hardDependencies['enterprise5/qimageblitz-e5'] = 'default'
        self.hardDependencies['enterprise5/soprano-e5'] = 'default'
        self.hardDependencies['enterprise5/strigi-e5'] = 'default'
        self.hardDependencies['enterprise5/phonon-e5'] = 'default'
        self.hardDependencies['enterprise5/automoc-e5'] = 'default'
        self.hardDependencies['enterprise5/attica-e5'] = 'default'

        # Take dbusmenu-qt from kdesupport as long as there are no differences
        self.hardDependencies['kdesupport/dbusmenu-qt'] = 'default'

        self.hardDependencies['win32libs-sources/libbzip2-src']  = 'default'
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
        self.hardDependencies['data/docbook-xsl'] = 'default'
        self.hardDependencies['data/docbook-dtd'] = 'default'

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
