
import utils
import sys
import info

class subinfo(info.infoclass):
    def setDependencies( self ):
        self.buildDependencies['virtual/base'] = 'default'
        self.dependencies['win32libs/taglib'] = 'default'
        self.shortDescription = "more plugins for the taglib library"

    def setTargets( self ):
        self.svnTargets['svnHEAD'] = 'trunk/kdesupport/taglib-extras'
        self.targets['1.0.1'] = 'http://kollide.net/~jefferai/taglib-extras-1.0.1.tar.gz'
        self.targetInstSrc['1.0.1'] = 'taglib-extras-1.0.1'
        self.patchToApply['1.0.1'] = [("taglib-extras-1.0.1-20130310.diff", 1)]
        self.defaultTarget = '1.0.1'


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__( self ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )
        self.subinfo.options.configure.defines = ""
#        self.subinfo.options.configure.defines += "-DWITH_KDE=ON"

if __name__ == '__main__':
    Package().execute()
