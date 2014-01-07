from Package.VirtualPackageBase import *
import info
import emergePlatform

class subinfo(info.infoclass):
    def setTargets( self ):
        self.targets['0.1'] = ""
        self.defaultTarget = '0.1'

    def setDependencies( self ):
        self.dependencies['win32libs/aspell']  = 'default'
#        self.dependencies['win32libs/enchant']  = 'default'
        self.dependencies['win32libs/gettext']  = 'default'
        self.dependencies['win32libs/giflib']  = 'default'
#        self.dependencies['win32libs/gssapi']  = 'default'
#        self.dependencies['win32libs/hspell']  = 'default'
        if not emergePlatform.isCrossCompilingEnabled():
            self.dependencies['win32libs/jasper']  = 'default'
        self.dependencies['win32libs/jpeg']  = 'default'
        self.dependencies['win32libs/libbzip2']  = 'default'
        self.dependencies['win32libs/libpng']  = 'default'
        self.dependencies['win32libs/libxml2']  = 'default'
        self.dependencies['win32libs/libxslt']  = 'default'
#        self.dependencies['win32libs/openexr']  = 'default'
        self.dependencies['win32libs/openssl']  = 'default'
        self.dependencies['win32libs/pcre']  = 'default'
        self.dependencies['win32libs/shared-mime-info']  = 'default'
        self.dependencies['win32libs/zlib']  = 'default'

class Package( VirtualPackageBase ):
    def __init__( self ):
        self.subinfo = subinfo()
        VirtualPackageBase.__init__( self )

if __name__ == '__main__':
    Package().execute()
