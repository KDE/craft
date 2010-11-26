from Package.VirtualPackageBase import *
import info
import emergePlatform

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.1'] = ""
        self.defaultTarget = '0.1'
    
    def setDependencies( self ):
        self.dependencies['win32libs-bin/aspell']  = 'default'
#        self.dependencies['win32libs-bin/enchant']  = 'default'
        self.dependencies['win32libs-bin/gettext']  = 'default'
        self.dependencies['win32libs-bin/giflib']  = 'default'
#        self.dependencies['win32libs-bin/gssapi']  = 'default'
#        self.dependencies['win32libs-bin/hspell']  = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs-bin/jasper']  = 'default'
        self.dependencies['win32libs-bin/jpeg']  = 'default'
        self.dependencies['win32libs-bin/libbzip2']  = 'default'
        self.dependencies['win32libs-bin/libpng']  = 'default'
        self.dependencies['win32libs-bin/libxml2']  = 'default'
        self.dependencies['win32libs-bin/libxslt']  = 'default'
#        self.dependencies['win32libs-bin/openexr']  = 'default'
        self.dependencies['win32libs-bin/openssl']  = 'default'
        self.dependencies['win32libs-bin/pcre']  = 'default'
        self.dependencies['win32libs-bin/shared-mime-info']  = 'default'
        self.dependencies['win32libs-bin/zlib']  = 'default'
    
class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
