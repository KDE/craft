import sys
import base
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.hardDependencies['virtual/base'] = 'default'
        self.hardDependencies['libs/qt'] = 'default'
        self.hardDependencies['win32libs-sources/libpng-src'] = 'default'
        self.hardDependencies['win32libs-bin/zlib'] = 'default'

    def setTargets( self ):
        self.svnTargets['gitHEAD'] = '[git]kde:kdewin'
        self.svnTargets['0.3.9'] = 'tags/kdewin32/0.3.9'
        self.svnTargets['20091111'] = 'tags/kdepim/pe5.20091111/kdesupport/kdewin'
        self.svnTargets['20091123'] = 'tags/kdepim/pe5.20091123/kdesupport/kdewin'
        self.svnTargets['20091201'] = 'tags/kdepim/pe5.20091201/kdesupport/kdewin'
        self.svnTargets['20100101'] = 'tags/kdepim/enterprise5.0.20100101.1068602/kdesupport/kdewin'
        self.svnTargets['20100115'] = 'tags/kdepim/enterprise5.0.20100115.1075215/kdesupport/kdewin'
        self.svnTargets['20100122'] = 'tags/kdepim/enterprise5.0.20100122.1078631/kdesupport/kdewin'
        self.svnTargets['20100129'] = 'tags/kdepim/enterprise5.0.20100129.1082020/kdesupport/kdewin'
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/kdewin'
        self.svnTargets['20100205'] = 'tags/kdepim/enterprise5.0.20100205.1085631/kdesupport/kdewin'
        self.svnTargets['20100212'] = 'tags/kdepim/enterprise5.0.20100212.1089060/kdesupport/kdewin'
        self.defaultTarget = 'gitHEAD'

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self, **args ):
        CMakePackageBase.__init__( self, args=args )
        self.subinfo = subinfo()
        self.subinfo.options.configure.defines = (
                " -DBUILD_BASE_LIB_WITH_QT=ON "
                " -DBUILD_QT_LIB=ON "
                " -DBUILD_TOOLS=ON " )
        if compiler.isMinGW_W32():
            self.subinfo.options.configure.defines += " -DMINGW_W32=ON "

if __name__ == '__main__':
    Package().execute()
