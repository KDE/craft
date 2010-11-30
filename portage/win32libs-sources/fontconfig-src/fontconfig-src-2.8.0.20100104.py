import info

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['2.8.0'] = "http://fontconfig.org/release/fontconfig-2.8.0.tar.gz"
        self.patchToApply['2.8.0'] = ('fontconfig-2.8.0.diff', 1)
        self.targetInstSrc['2.8.0'] = "fontconfig-2.8.0"
        self.shortDescription = "library for font customization and configuration"
        self.defaultTarget = '2.8.0'
    
    def setDependencies( self ):
        self.dependencies['kdesupport/kdewin'] = 'default'
        self.dependencies['win32libs-bin/freetype'] = 'default'
        self.dependencies['win32libs-bin/libxml2'] = 'default'
    
from Package.CMakePackageBase import *
class Package(CMakePackageBase):
    def __init__( self, **args ):
        self.subinfo = subinfo()
        CMakePackageBase.__init__( self )

if __name__ == '__main__':
  Package().execute()
