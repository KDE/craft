import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.8.0-1'] = "http://fontconfig.org/release/fontconfig-2.8.0.tar.gz"
        self.patchToApply['2.8.0-1'] = ('fontconfig-2.8.0.diff', 1)
        self.targetInstSrc['2.8.0-1'] = "fontconfig-2.8.0"
        self.defaultTarget = '2.8.0-1'
    
    def setDependencies( self ):
        self.hardDependencies['kdesupport/kdewin'] = 'default'
        self.hardDependencies['win32libs-sources/freetype-src'] = 'default'
        self.hardDependencies['win32libs-sources/libxml2-src'] = 'default'
    
from Package.CMakePackageBase import *
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
  Package().execute()
